<script>
	import { onMount } from "svelte";

	const API_URL = "http://localhost:8000/api/proxy";

	let darkMode = true;
	let currentView = "login";
	let user = null;
	let posts = [];
	let loading = false;
	let newPostContent = "";
	let errorMessage = "";
	let accessToken = "";
	let authStep = "instance";
	let authCode = "";
	let notifications = [];
	let activeTab = "home";
	let trendingHashtags = [
		"technology",
		"opensource",
		"design",
		"ai",
		"webdev",
	];

	let clientData = null;
	let selectedInstance = "";
	let mobileMenuOpen = false;

	function toggleTheme() {
		darkMode = !darkMode;
		document.documentElement.classList.toggle("dark", darkMode);
	}

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}

	onMount(() => {
		const savedUser = localStorage.getItem("rettoUser");
		const savedToken = localStorage.getItem("rettoToken");

		if (savedUser && savedToken) {
			user = JSON.parse(savedUser);
			accessToken = savedToken;
			selectedInstance = user.acct.split('@')[1] || "mastodon.social";
			currentView = "timeline";
			loadTimeline();
		}
		document.documentElement.classList.toggle("dark", darkMode);

		loadTrendingData();
	});

	async function selectInstance(instance) {
		selectedInstance = instance;
		errorMessage = "";
		loading = true;

		try {
			const response = await fetch(
				`http://localhost:8000/api/proxy/apps`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						instance: instance,
					}),
				},
			);

			if (!response.ok) {
				throw new Error("API error");
			}

			clientData = await response.json();

			if (!clientData.client_id) {
				throw new Error("Invalid response");
			}

			const authUrl = `https://${instance}/oauth/authorize?client_id=${clientData.client_id}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&scope=read+write+follow`;

			authStep = "authorize";

			window.open(authUrl, "_blank");
		} catch (error) {
			errorMessage = "Instance bağlantı hatası: " + error.message;
			console.error("Auth error:", error);
		}

		loading = false;
	}

	async function completeAuth() {
		if (!authCode.trim()) {
			errorMessage = "Lütfen authorization kodunu girin";
			return;
		}

		loading = true;

		try {
			const response = await fetch(
				`http://localhost:8000/api/proxy/token`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						instance: selectedInstance,
						client_id: clientData.client_id,
						client_secret: clientData.client_secret,
						redirect_uri: "urn:ietf:wg:oauth:2.0:oob",
						grant_type: "authorization_code",
						code: authCode,
						scope: "read write follow",
					}),
				},
			);

			if (response.ok) {
				const tokenData = await response.json();
				accessToken = tokenData.access_token;

				const userResponse = await fetch(
					`https://${selectedInstance}/api/v1/accounts/verify_credentials`,
					{
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					},
				);

				if (userResponse.ok) {
					user = await userResponse.json();

					localStorage.setItem("rettoUser", JSON.stringify(user));
					localStorage.setItem("rettoToken", accessToken);

					currentView = "timeline";
					authStep = "instance";
					await loadTimeline();
				}
			} else {
				errorMessage = "Authorization failed";
			}
		} catch (error) {
			errorMessage = "Bağlantı hatası: " + error.message;
		}

		loading = false;
	}

	async function loadTimeline() {
		if (!accessToken) {
			await loadPublicTimeline();
			return;
		}

		loading = true;

		try {
			const endpoint = activeTab === "home" ? "home" : "public";
			const response = await fetch(
				`http://localhost:8000/api/proxy/timeline/${selectedInstance}?endpoint=${endpoint}&limit=20`,
				{
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				},
			);

			if (response.ok) {
				const timelineData = await response.json();
				posts = timelineData.map((post) => ({
					id: post.id,
					content: post.content,
					created_at: post.created_at,
					media_attachments: post.media_attachments || [],
					reblogs_count: post.reblogs_count || 0,
					favourites_count: post.favourites_count || 0,
					replies_count: post.replies_count || 0,
					favourited: post.favourited || false,
					reblogged: post.reblogged || false,
					account: {
						username: post.account.username,
						display_name: post.account.display_name,
						avatar: post.account.avatar,
						acct: post.account.acct,
						followers_count: post.account.followers_count,
						following_count: post.account.following_count,
						statuses_count: post.account.statuses_count,
					},
				}));
			} else {
				await loadPublicTimeline();
			}
		} catch (error) {
			console.error("Timeline error:", error);
			await loadPublicTimeline();
		}

		loading = false;
	}

	async function loadPublicTimeline() {
		loading = true;
		try {
			const response = await fetch(
				`http://localhost:8000/api/proxy/timeline/${selectedInstance}?endpoint=public&limit=20`,
			);
			if (response.ok) {
				const timelineData = await response.json();
				posts = timelineData.map((post) => ({
					id: post.id,
					content: post.content,
					created_at: post.created_at,
					media_attachments: post.media_attachments || [],
					reblogs_count: post.reblogs_count || 0,
					favourites_count: post.favourites_count || 0,
					replies_count: post.replies_count || 0,
					favourited: post.favourited || false,
					reblogged: post.reblogged || false,
					account: {
						username: post.account.username,
						display_name: post.account.display_name,
						avatar: post.account.avatar,
						acct: post.account.acct,
						followers_count: post.account.followers_count,
						following_count: post.account.following_count,
						statuses_count: post.account.statuses_count,
					},
				}));
			}
		} catch (error) {
			console.error("Public timeline error:", error);
		}
		loading = false;
	}

	async function postStatus() {
		if (!newPostContent.trim() || !accessToken) return;

		loading = true;

		try {
			const response = await fetch(
				`https://${selectedInstance}/api/v1/statuses`,
				{
					method: "POST",
					headers: {
						Authorization: `Bearer ${accessToken}`,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						status: newPostContent,
					}),
				},
			);

			if (response.ok) {
				newPostContent = "";
				await loadTimeline();
				errorMessage = "";
			} else {
				errorMessage = "Gönderi paylaşılamadı";
			}
		} catch (error) {
			errorMessage = "Bağlantı hatası";
		}

		loading = false;
	}

	async function likePost(post) {
		if (!accessToken) return;

		try {
			if (post.favourited) {
				await fetch(
					`https://${selectedInstance}/api/v1/statuses/${post.id}/unfavourite`,
					{
						method: "POST",
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					},
				);
				post.favourites_count = Math.max(0, post.favourites_count - 1);
				post.favourited = false;
			} else {
				await fetch(
					`https://${selectedInstance}/api/v1/statuses/${post.id}/favourite`,
					{
						method: "POST",
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					},
				);
				post.favourites_count = (post.favourites_count || 0) + 1;
				post.favourited = true;
			}
		} catch (error) {
			console.error("Like error");
		}
	}

	async function reblogPost(post) {
		if (!accessToken) return;

		try {
			if (post.reblogged) {
				await fetch(
					`https://${selectedInstance}/api/v1/statuses/${post.id}/unreblog`,
					{
						method: "POST",
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					},
				);
				post.reblogs_count = Math.max(0, post.reblogs_count - 1);
				post.reblogged = false;
			} else {
				await fetch(
					`https://${selectedInstance}/api/v1/statuses/${post.id}/reblog`,
					{
						method: "POST",
						headers: {
							Authorization: `Bearer ${accessToken}`,
						},
					},
				);
				post.reblogs_count = (post.reblogs_count || 0) + 1;
				post.reblogged = true;
			}
		} catch (error) {
			console.error("Reblog error");
		}
	}

	function loadTrendingData() {
		trendingHashtags = [
			"technology",
			"opensource",
			"design",
			"ai",
			"webdev",
			"fediverse",
			"privacy",
		];
	}

	function logout() {
		user = null;
		accessToken = "";
		posts = [];
		currentView = "login";
		errorMessage = "";
		authStep = "instance";
		authCode = "";
		mobileMenuOpen = false;
		localStorage.removeItem("rettoUser");
		localStorage.removeItem("rettoToken");
	}

	function formatDate(dateString) {
		return new Date(dateString).toLocaleDateString("tr-TR", {
			hour: "2-digit",
			minute: "2-digit",
			day: "numeric",
			month: "short",
		});
	}

	function formatNumber(num) {
		if (!num) return "0";
		if (num >= 1000000) {
			return (num / 1000000).toFixed(1) + "M";
		}
		if (num >= 1000) {
			return (num / 1000).toFixed(1) + "K";
		}
		return num.toString();
	}
</script>

<div
	class="min-h-screen transition-all duration-500 {darkMode
		? 'dark bg-gradient-to-br from-gray-900 via-black to-red-900'
		: 'bg-gradient-to-br from-red-50 via-white to-gray-100'}"
>
	{#if currentView === "login"}
		<div
			class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden"
		>
			<div
				class="absolute inset-0 bg-gradient-to-br from-red-500/10 via-transparent to-black/30"
			></div>
			<div
				class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-red-500/5 via-transparent to-transparent"
			></div>

			<div class="w-full max-w-md relative z-10">
				<div class="text-center mb-8">
					<div
						class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-red-600 to-black rounded-3xl mb-4 shadow-2xl"
					>
						<span class="text-3xl font-black text-white">R</span>
					</div>
					<h1
						class="text-6xl font-black bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent mb-2"
					>
						RETTO
					</h1>
					<p
						class="text-xl {darkMode
							? 'text-red-200/80'
							: 'text-red-600/80'} font-light"
					>
						Modern Fediverse Deneyimi
					</p>
				</div>

				<div
					class="backdrop-blur-xl bg-white/10 dark:bg-black/20 border border-white/20 dark:border-red-500/20 rounded-3xl shadow-2xl p-8"
				>
					{#if authStep === "instance"}
						<div class="space-y-6">
							<div class="text-center">
								<h2 class="text-2xl font-bold text-white mb-2">
									Instance Seçin
								</h2>
								<p class="text-red-200/60">
									Fediverse'a bağlanmak için bir instance seçin
								</p>
							</div>

							<div class="space-y-4">
								<button
									on:click={() => selectInstance("mastodon.social")}
									disabled={loading}
									class="w-full bg-white/5 hover:bg-white/10 border border-white/10 hover:border-red-500/50 text-white py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center space-x-3"
								>
									<span class="text-xl">🐘</span>
									<span>Mastodon.social ile Giriş</span>
								</button>

								<button
									on:click={() => selectInstance("fosstodon.org")}
									disabled={loading}
									class="w-full bg-white/5 hover:bg-white/10 border border-white/10 hover:border-red-500/50 text-white py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center space-x-3"
								>
									<span class="text-xl">🔧</span>
									<span>Fosstodon.org ile Giriş</span>
								</button>
							</div>

							<div class="text-center pt-4 border-t border-white/10">
								<p class="text-red-200/50 text-sm">
									Hesabınız yok mu? Seçtiğiniz instance'ın web sitesinden kayıt olabilirsiniz.
								</p>
								<div class="flex justify-center space-x-6 mt-3">
									<a 
										href="https://mastodon.social/auth/sign_up" 
										target="_blank" 
										class="text-red-300 hover:text-red-200 text-sm underline transition-colors"
									>
										mastodon.social'da kayıt ol
									</a>
									<a 
										href="https://fosstodon.org/auth/sign_up" 
										target="_blank" 
										class="text-red-300 hover:text-red-200 text-sm underline transition-colors"
									>
										fosstodon.org'da kayıt ol
									</a>
								</div>
							</div>

							{#if loading}
								<div class="flex items-center justify-center py-4">
									<div class="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
									<span class="text-white">Bağlanıyor...</span>
								</div>
							{/if}
						</div>
					{:else}
						<div class="space-y-6">
							<div class="text-center">
								<div
									class="w-16 h-16 bg-green-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4"
								>
									<span class="text-2xl">✅</span>
								</div>
								<h2 class="text-2xl font-bold text-white mb-2">
									Authorization Gerekli
								</h2>
								<p class="text-red-200/60">
									Yeni pencerede giriş yapıp authorization
									kodunu alın
								</p>
							</div>

							<div
								class="bg-yellow-500/20 border border-yellow-500/30 rounded-2xl p-4"
							>
								<p class="text-yellow-200 text-sm">
									<strong>Not:</strong> Authorization sayfasında
									"AUTHORIZE" butonuna tıkladıktan sonra alacağınız
									kodu aşağıya girin.
								</p>
							</div>

							<div>
								<input
									bind:value={authCode}
									class="w-full px-4 py-4 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20 text-lg text-center font-mono"
									placeholder="Authorization kodunu yapıştırın"
								/>
							</div>

							<div class="flex space-x-3">
								<button
									on:click={() => (authStep = "instance")}
									class="flex-1 bg-gray-600/80 hover:bg-gray-500 text-white py-3 px-4 rounded-2xl font-semibold transition-all duration-300"
								>
									Geri
								</button>
								<button
									on:click={completeAuth}
									disabled={loading}
									class="flex-1 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 disabled:from-gray-600 disabled:to-gray-700 text-white py-3 px-4 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:scale-100"
								>
									{#if loading}
										<span
											class="flex items-center justify-center"
										>
											<div
												class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"
											></div>
											Giriş yapılıyor...
										</span>
									{:else}
										Tamamla
									{/if}
								</button>
							</div>
						</div>
					{/if}

					{#if errorMessage}
						<div
							class="mt-6 p-4 bg-red-500/20 border border-red-500/30 text-red-100 rounded-2xl backdrop-blur-sm"
						>
							<div class="flex items-center">
								<div
									class="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center mr-3"
								>
									<span class="text-xs font-bold">!</span>
								</div>
								{errorMessage}
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{:else}
		<div class="flex flex-col lg:flex-row h-screen bg-gradient-to-br from-gray-900 via-black to-red-900">
			<div class="lg:hidden fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-black/80 border-b border-red-500/20 p-4">
				<div class="flex items-center justify-between">
					<div class="flex items-center space-x-3">
						<div class="w-10 h-10 bg-gradient-to-br from-red-600 to-black rounded-2xl flex items-center justify-center">
							<span class="text-lg font-black text-white">R</span>
						</div>
						<h1 class="text-xl font-black bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent">
							Retto
						</h1>
					</div>
					<button on:click={toggleMobileMenu} class="p-2 text-white">
						{#if mobileMenuOpen}
							<span class="text-2xl">✕</span>
						{:else}
							<span class="text-2xl">☰</span>
						{/if}
					</button>
				</div>
			</div>

			<div class="hidden lg:flex lg:w-80 backdrop-blur-xl bg-black/40 border-r border-red-500/20 flex-col h-full">
				<div class="p-6 border-b border-red-500/20">
					<div class="flex items-center space-x-3">
						<div class="w-12 h-12 bg-gradient-to-br from-red-600 to-black rounded-2xl flex items-center justify-center shadow-2xl">
							<span class="text-xl font-black text-white">R</span>
						</div>
						<h1 class="text-2xl font-black bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent">
							Retto
						</h1>
					</div>
				</div>

				<div class="flex-1 p-6 overflow-y-auto">
					<nav class="space-y-2">
						<button
							class="w-full flex items-center space-x-3 p-4 rounded-2xl hover:bg-red-500/20 transition-all duration-300 {activeTab === 'home' ? 'bg-red-500/30 border border-red-500/50' : ''}"
							on:click={() => {
								activeTab = "home";
								loadTimeline();
							}}
						>
							<span class="text-2xl">🏠</span>
							<span class="font-semibold text-white">Ana Sayfa</span>
						</button>
						<button
							class="w-full flex items-center space-x-3 p-4 rounded-2xl hover:bg-red-500/20 transition-all duration-300 {activeTab === 'explore' ? 'bg-red-500/30 border border-red-500/50' : ''}"
							on:click={() => {
								activeTab = "explore";
								loadPublicTimeline();
							}}
						>
							<span class="text-2xl">🔍</span>
							<span class="font-semibold text-white">Keşfet</span>
						</button>
					</nav>

					<div class="mt-8">
						<h3 class="text-lg font-bold text-white mb-4">Trend Konular</h3>
						<div class="space-y-2">
							{#each trendingHashtags as tag}
								<button class="w-full text-left p-3 rounded-xl hover:bg-red-500/20 transition-all duration-300">
									<span class="text-red-400 font-medium">#{tag}</span>
									<span class="text-red-200/60 text-sm block">Trending</span>
								</button>
							{/each}
						</div>
					</div>
				</div>

				{#if user}
					<div class="p-6 border-t border-red-500/20 bg-black/40">
						<div class="flex items-center space-x-3 mb-4">
							<img src={user.avatar} alt={user.username} class="w-12 h-12 rounded-2xl border-2 border-red-500/30" />
							<div class="flex-1 min-w-0">
								<div class="font-bold text-white truncate">{user.display_name}</div>
								<div class="text-red-200/60 text-sm truncate">@{user.acct}</div>
							</div>
						</div>
						<div class="grid grid-cols-3 gap-2 text-center mb-4">
							<div class="bg-black/40 rounded-xl p-2">
								<div class="font-bold text-white">{formatNumber(user.statuses_count)}</div>
								<div class="text-red-200/60 text-xs">Gönderi</div>
							</div>
							<div class="bg-black/40 rounded-xl p-2">
								<div class="font-bold text-white">{formatNumber(user.following_count)}</div>
								<div class="text-red-200/60 text-xs">Takip</div>
							</div>
							<div class="bg-black/40 rounded-xl p-2">
								<div class="font-bold text-white">{formatNumber(user.followers_count)}</div>
								<div class="text-red-200/60 text-xs">Takipçi</div>
							</div>
						</div>
						<div class="flex space-x-2">
							<button style="display: none !important;" on:click={toggleTheme} class="flex-1 p-2 bg-black/40 border border-red-500/20 rounded-xl hover:bg-red-500/20 transition-all duration-300">
								{#if darkMode}
									<span class="text-lg">☀️</span>
								{:else}
									<span class="text-lg">🌙</span>
								{/if}
							</button>
							<button on:click={logout} class="flex-1 bg-red-600/80 hover:bg-red-500 text-white p-2 rounded-xl font-medium transition-all duration-300">
								Çıkış
							</button>
						</div>
					</div>
				{/if}
			</div>

			{#if mobileMenuOpen}
				<div class="lg:hidden fixed inset-0 z-40 bg-black/80 backdrop-blur-lg pt-20">
					<div class="p-6 space-y-4">
						<button
							class="w-full flex items-center space-x-3 p-4 rounded-2xl bg-red-500/30 border border-red-500/50 text-white"
							on:click={() => {
								activeTab = "home";
								loadTimeline();
								mobileMenuOpen = false;
							}}
						>
							<span class="text-2xl">🏠</span>
							<span class="font-semibold">Ana Sayfa</span>
						</button>
						<button
							class="w-full flex items-center space-x-3 p-4 rounded-2xl hover:bg-red-500/20 text-white transition-all duration-300"
							on:click={() => {
								activeTab = "explore";
								loadPublicTimeline();
								mobileMenuOpen = false;
							}}
						>
							<span class="text-2xl">🔍</span>
							<span class="font-semibold">Keşfet</span>
						</button>
						<div class="pt-4 border-t border-red-500/20">
							<div class="flex items-center space-x-3 p-4">
								<img src={user.avatar} alt={user.username} class="w-10 h-10 rounded-2xl border-2 border-red-500/30" />
								<div class="flex-1">
									<div class="font-bold text-white truncate">{user.display_name}</div>
									<div class="text-red-200/60 text-sm truncate">@{user.acct}</div>
								</div>
							</div>
							<button on:click={logout} class="w-full bg-red-600/80 hover:bg-red-500 text-white p-3 rounded-xl font-medium transition-all duration-300 mt-4">
								Çıkış Yap
							</button>
						</div>
					</div>
				</div>
			{/if}

			<div class="flex-1 flex flex-col overflow-hidden lg:mt-0 mt-16">
				<header class="backdrop-blur-xl bg-black/40 border-b border-red-500/20 p-4 lg:p-6">
					<div class="flex items-center justify-between">
						<h2 class="text-xl lg:text-2xl font-bold text-white">
							{#if activeTab === "home"}
								🏠 Ana Sayfa
							{:else}
								🔍 Keşfet
							{/if}
						</h2>
						<div class="flex items-center space-x-4">
							<div class="relative hidden lg:block">
								<input type="text" placeholder="Ara..." class="px-4 py-2 rounded-2xl bg-black/40 border border-red-500/20 text-white placeholder-red-200/50 backdrop-blur-sm w-64" />
							</div>
							<button on:click={toggleTheme} class="p-2 text-white lg:hidden">
								{#if darkMode}
									<span class="text-lg">☀️</span>
								{:else}
									<span class="text-lg">🌙</span>
								{/if}
							</button>
						</div>
					</div>
				</header>

				<main class="flex-1 overflow-y-auto bg-gradient-to-br from-gray-900/50 via-black/50 to-red-900/50">
					<div class="max-w-2xl mx-auto p-4 lg:p-6">
						{#if user}
							<div class="mb-6 lg:mb-8 rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl overflow-hidden">
								<div class="p-4 lg:p-6">
									<div class="flex space-x-4">
										<img src={user.avatar} alt={user.username} class="w-10 h-10 lg:w-12 lg:h-12 rounded-2xl border-2 border-red-500/30" />
										<div class="flex-1">
											<textarea bind:value={newPostContent} placeholder="Dünyaya ne haber veriyorsun?" class="w-full h-20 px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20 resize-none" />
											<div class="flex justify-between items-center mt-4">
												<div class="flex space-x-2">
													<button class="p-2 hover:bg-red-500/20 rounded-xl transition-colors">
														<span class="text-xl">🖼️</span>
													</button>
												</div>
												<button on:click={postStatus} disabled={loading || !newPostContent.trim()} class="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 disabled:from-gray-600 disabled:to-gray-700 text-white px-4 lg:px-6 py-2 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg disabled:shadow-none text-sm lg:text-base">
													{#if loading}
														<span class="flex items-center">
															<div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
															Paylaşılıyor...
														</span>
													{:else}
														Paylaş
													{/if}
												</button>
											</div>
										</div>
									</div>
								</div>
							</div>
						{/if}

						<div class="space-y-4 lg:space-y-6">
							{#if loading && posts.length === 0}
								<div class="text-center py-12">
									<div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-black rounded-2xl mb-4 shadow-2xl animate-pulse">
										<span class="text-2xl font-bold text-white">R</span>
									</div>
									<p class="text-red-200/60 mt-4">Gönderiler yükleniyor...</p>
								</div>
							{:else if posts.length > 0}
								{#each posts as post}
									<div class="rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl overflow-hidden transition-all duration-500 hover:border-red-500/40 hover:shadow-2xl">
										<div class="p-4 lg:p-6">
											<div class="flex items-start space-x-3 lg:space-x-4">
												<img src={post.account.avatar} alt={post.account.username} class="w-10 h-10 lg:w-12 lg:h-12 rounded-2xl border-2 border-red-500/30 shadow-lg flex-shrink-0" />
												<div class="flex-1 min-w-0">
													<div class="flex items-start justify-between mb-3">
														<div class="flex-1">
															<div class="flex flex-col lg:flex-row lg:items-center space-y-1 lg:space-y-0 lg:space-x-2 mb-1">
																<span class="font-bold text-white text-base lg:text-lg">{post.account.display_name}</span>
																<span class="text-red-200/60 text-sm">@{post.account.acct}</span>
															</div>
															<span class="text-red-200/40 text-sm">{formatDate(post.created_at)}</span>
														</div>
														<button class="p-2 hover:bg-red-500/20 rounded-xl transition-colors flex-shrink-0">
															<span class="text-xl">⋯</span>
														</button>
													</div>

													<div class="text-white/90 leading-relaxed mb-4 text-sm lg:text-base">
														{@html post.content}
													</div>

													{#if post.media_attachments.length > 0}
														<div class="mb-4 grid gap-2 {post.media_attachments.length === 1 ? 'grid-cols-1' : 'grid-cols-2'}">
															{#each post.media_attachments as media}
																{#if media.type === "image"}
																	<img src={media.url} alt="Gönderi resmi" class="rounded-2xl border border-white/10 shadow-lg hover:scale-105 transition-transform duration-300 cursor-zoom-in max-h-96 object-cover w-full" />
																{/if}
															{/each}
														</div>
													{/if}

													<div class="flex items-center justify-between pt-4 border-t border-red-500/20">
														<button on:click={() => reblogPost(post)} class="flex items-center space-x-2 {post.reblogged ? 'text-green-400' : 'text-red-200/60 hover:text-green-400'} transition-colors">
															<span class="text-xl">{post.reblogged ? '🔁' : '🔄'}</span>
															<span class="text-sm lg:text-base">{formatNumber(post.reblogs_count)}</span>
														</button>
														<button on:click={() => likePost(post)} class="flex items-center space-x-2 {post.favourited ? 'text-red-400' : 'text-red-200/60 hover:text-red-400'} transition-colors">
															<span class="text-xl">{post.favourited ? '❤️' : '🤍'}</span>
															<span class="text-sm lg:text-base">{formatNumber(post.favourites_count)}</span>
														</button>
														<button class="flex items-center space-x-2 text-red-200/60 hover:text-blue-400 transition-colors">
															<span class="text-xl">💬</span>
															<span class="text-sm lg:text-base">{formatNumber(post.replies_count)}</span>
														</button>
														<button class="flex items-center space-x-2 text-red-200/60 hover:text-yellow-400 transition-colors">
															<span class="text-xl">📤</span>
														</button>
													</div>
												</div>
											</div>
										</div>
									</div>
								{/each}
							{:else}
								<div class="text-center py-12">
									<div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-black rounded-2xl mb-4 shadow-2xl">
										<span class="text-2xl font-bold text-white">R</span>
									</div>
									<p class="text-red-200/60">Henüz gönderi yok</p>
								</div>
							{/if}
						</div>
					</div>
				</main>
			</div>
		</div>
	{/if}
</div>