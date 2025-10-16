<script>
    import { onMount } from 'svelte';
    
    let darkMode = true;
    let currentView = 'login';
    let user = null;
    let posts = [];
    let loading = false;
    let newPostContent = '';
    let loginData = { username: '', password: '' };
    let registerData = { username: '', email: '', password: '', confirmPassword: '' };
    let timelineType = 'public';
    let errorMessage = '';

    const DEFAULT_INSTANCE = 'mastodon.social';

    function toggleTheme() {
        darkMode = !darkMode;
        document.documentElement.classList.toggle('dark', darkMode);
    }

    onMount(() => {
        const savedUser = localStorage.getItem('socialUser');
        if (savedUser) {
            user = JSON.parse(savedUser);
            currentView = 'timeline';
            loadTimeline();
        }
        document.documentElement.classList.toggle('dark', darkMode);
    });

    async function handleRegister() {
        errorMessage = '';

        if (!registerData.username || !registerData.email || !registerData.password) {
            errorMessage = 'Tüm alanları doldurun';
            return;
        }

        if (registerData.password.length < 6) {
            errorMessage = 'Şifre en az 6 karakter olmalı';
            return;
        }

        if (registerData.password !== registerData.confirmPassword) {
            errorMessage = 'Şifreler eşleşmiyor';
            return;
        }

        loading = true;

        try {
            const appResponse = await fetch(`https://${DEFAULT_INSTANCE}/api/v1/apps`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    client_name: 'Retto Social',
                    redirect_uris: 'urn:ietf:wg:oauth:2.0:oob',
                    scopes: 'read write follow',
                    website: 'https://retto.social'
                })
            });

            const appData = await appResponse.json();

            const newUser = {
                id: Date.now(),
                username: registerData.username,
                email: registerData.email,
                display_name: registerData.username,
                avatar: `https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&h=150&fit=crop&crop=face&bg=linear-gradient(45deg, #dc2626, #000000)`,
                instance: DEFAULT_INSTANCE,
                access_token: 'demo_token_' + Date.now()
            };

            const existingUsers = JSON.parse(localStorage.getItem('socialUsers') || '[]');
            existingUsers.push(newUser);
            localStorage.setItem('socialUsers', JSON.stringify(existingUsers));
            localStorage.setItem('socialUser', JSON.stringify(newUser));

            user = newUser;
            currentView = 'timeline';
            await loadTimeline();

        } catch (error) {
            errorMessage = 'Kayıt işlemi sırasında bir hata oluştu';
        }

        loading = false;
    }

    async function handleLogin() {
        errorMessage = '';

        if (!loginData.username || !loginData.password) {
            errorMessage = 'Kullanıcı adı ve şifre gerekli';
            return;
        }

        loading = true;

        try {
            const existingUsers = JSON.parse(localStorage.getItem('socialUsers') || '[]');
            const foundUser = existingUsers.find(u => u.username === loginData.username);

            if (foundUser) {
                user = foundUser;
                localStorage.setItem('socialUser', JSON.stringify(user));
                currentView = 'timeline';
                await loadTimeline();
            } else {
                errorMessage = 'Kullanıcı adı veya şifre hatalı';
            }

        } catch (error) {
            errorMessage = 'Giriş işlemi sırasında bir hata oluştu';
        }

        loading = false;
    }

    async function loadTimeline() {
        if (!user) return;
        
        loading = true;

        try {
            const endpoint = timelineType === 'home' ? 'home' : 'public';
            const response = await fetch(`https://${DEFAULT_INSTANCE}/api/v1/timelines/${endpoint}?limit=20`);
            
            if (response.ok) {
                const mastodonPosts = await response.json();
                
                posts = mastodonPosts.map(post => ({
                    id: post.id,
                    content: post.content,
                    created_at: post.created_at,
                    media_attachments: post.media_attachments || [],
                    account: {
                        username: post.account.username,
                        display_name: post.account.display_name || post.account.username,
                        avatar: post.account.avatar,
                        acct: post.account.acct
                    }
                }));
            } else {
                loadDemoPosts();
            }
        } catch (error) {
            loadDemoPosts();
        }

        loading = false;
    }

    function loadDemoPosts() {
        posts = [
            {
                id: 1,
                content: 'Merhaba! Nexus Social ailesine hoş geldiniz! 🎉 Yeni nesil sosyal deneyim başlıyor.',
                created_at: new Date().toISOString(),
                media_attachments: [
                    {
                        type: 'image',
                        url: 'https://images.unsplash.com/photo-1579546929662-711aa81148cf?w=600&h=400&fit=crop',
                        preview_url: 'https://images.unsplash.com/photo-1579546929662-711aa81148cf?w=300&h=200&fit=crop'
                    }
                ],
                account: {
                    username: 'nexusofficial',
                    display_name: 'Nexus Social',
                    avatar: 'https://images.unsplash.com/photo-1611605698335-8b1569810432?w=150&h=150&fit=crop&crop=face',
                    acct: 'nexusofficial'
                }
            },
            {
                id: 2,
                content: 'Gece şehir manzarası ve yıldızlar... 🌃✨',
                created_at: new Date(Date.now() - 3600000).toISOString(),
                media_attachments: [
                    {
                        type: 'image',
                        url: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=600&h=400&fit=crop',
                        preview_url: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=300&h=200&fit=crop'
                    }
                ],
                account: {
                    username: 'nightphotographer',
                    display_name: 'Gece Fotoğrafçısı',
                    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
                    acct: 'nightphotographer'
                }
            },
            {
                id: 3,
                content: 'Doğanın güzellikleri karşısında hayran kalmamak elde değil! 🏞️',
                created_at: new Date(Date.now() - 7200000).toISOString(),
                media_attachments: [
                    {
                        type: 'image',
                        url: 'https://images.unsplash.com/photo-1501854140801-50d01698950b?w=600&h=400&fit=crop',
                        preview_url: 'https://images.unsplash.com/photo-1501854140801-50d01698950b?w=300&h=200&fit=crop'
                    }
                ],
                account: {
                    username: 'naturelover',
                    display_name: 'Doğa Aşığı',
                    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
                    acct: 'naturelover'
                }
            },
            {
                id: 4,
                content: 'Teknoloji ve tasarımın buluştuğu anlar... Bu proje gerçekten harika görünüyor! 💻✨',
                created_at: new Date(Date.now() - 10800000).toISOString(),
                media_attachments: [
                    {
                        type: 'image',
                        url: 'https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=600&h=400&fit=crop',
                        preview_url: 'https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=300&h=200&fit=crop'
                    }
                ],
                account: {
                    username: 'techdesigner',
                    display_name: 'Teknoloji Tasarımcısı',
                    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
                    acct: 'techdesigner'
                }
            }
        ];
    }

    async function postStatus() {
        if (!newPostContent.trim() || !user) return;
        
        loading = true;

        try {
            const newPost = {
                id: Date.now(),
                content: newPostContent,
                created_at: new Date().toISOString(),
                media_attachments: [],
                account: {
                    username: user.username,
                    display_name: user.display_name,
                    avatar: user.avatar,
                    acct: user.username
                }
            };
            
            posts = [newPost, ...posts];
            newPostContent = '';
            errorMessage = '';
            
        } catch (error) {
            errorMessage = 'Gönderi paylaşılırken bir hata oluştu';
        }

        loading = false;
    }

    function logout() {
        user = null;
        posts = [];
        currentView = 'login';
        loginData = { username: '', password: '' };
        registerData = { username: '', email: '', password: '', confirmPassword: '' };
        errorMessage = '';
        localStorage.removeItem('socialUser');
    }

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('tr-TR', {
            hour: '2-digit',
            minute: '2-digit',
            day: 'numeric',
            month: 'short'
        });
    }

    function createMarkup(html) {
        return { __html: html };
    }
</script>

<div class="min-h-screen transition-all duration-500 {darkMode ? 'dark bg-gradient-to-br from-gray-900 via-black to-red-900' : 'bg-gradient-to-br from-red-50 via-white to-gray-100'}">
    {#if currentView === 'login' || currentView === 'register'}
        <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
            <!-- Arka plan efekti -->
            <div class="absolute inset-0 bg-gradient-to-br from-red-500/10 via-transparent to-black/30"></div>
            <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-red-500/5 via-transparent to-transparent"></div>
            
            <div class="w-full max-w-md relative z-10">
                <div class="text-center mb-8">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-black rounded-2xl mb-4 shadow-2xl">
                        <span class="text-2xl font-bold text-white">N</span>
                    </div>
                    <h1 class="text-5xl font-black bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent mb-2">Retto</h1>
                    <p class="text-lg {darkMode ? 'text-red-200/80' : 'text-red-600/80'} font-light">Sosyal Deneyimin Yeni Boyutu</p>
                </div>

                <div class="backdrop-blur-xl bg-white/10 dark:bg-black/20 border border-white/20 dark:border-red-500/20 rounded-3xl shadow-2xl p-8">
                    <div class="flex mb-8 bg-white/10 dark:bg-red-500/10 rounded-2xl p-1">
                        <button 
                            class="flex-1 py-3 font-semibold rounded-xl transition-all duration-300 {currentView === 'login' ? 'bg-red-600 text-white shadow-lg' : 'text-red-100/70 hover:text-white'}"
                            on:click={() => { currentView = 'login'; errorMessage = ''; }}
                        >
                            Giriş Yap
                        </button>
                        <button 
                            class="flex-1 py-3 font-semibold rounded-xl transition-all duration-300 {currentView === 'register' ? 'bg-red-600 text-white shadow-lg' : 'text-red-100/70 hover:text-white'}"
                            on:click={() => { currentView = 'register'; errorMessage = ''; }}
                        >
                            Kayıt Ol
                        </button>
                    </div>

                    {#if errorMessage}
                        <div class="mb-6 p-4 bg-red-500/20 border border-red-500/30 text-red-100 rounded-2xl backdrop-blur-sm">
                            <div class="flex items-center">
                                <div class="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center mr-3">
                                    <span class="text-xs font-bold">!</span>
                                </div>
                                {errorMessage}
                            </div>
                        </div>
                    {/if}

                    {#if currentView === 'register'}
                        <div class="space-y-4">
                            <div>
                                <input 
                                    bind:value={registerData.username}
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="Kullanıcı adı"
                                />
                            </div>
                            <div>
                                <input 
                                    bind:value={registerData.email}
                                    type="email"
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="E-posta adresi"
                                />
                            </div>
                            <div>
                                <input 
                                    bind:value={registerData.password}
                                    type="password"
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="Şifre"
                                />
                            </div>
                            <div>
                                <input 
                                    bind:value={registerData.confirmPassword}
                                    type="password"
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="Şifre tekrar"
                                />
                            </div>
                            <button 
								on:click={handleRegister}
								disabled={loading}
								class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 disabled:from-gray-600 disabled:to-gray-700 text-white py-4 px-6 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl disabled:shadow-none"
							>
								{#if loading}
									<span class="flex items-center justify-center">
										<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
										Hesap oluşturuluyor...
									</span>
								{:else}
									Hesap Oluştur
								{/if}
							</button>
                        </div>
                    {:else}
                        <div class="space-y-4">
                            <div>
                                <input 
                                    bind:value={loginData.username}
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="Kullanıcı adı"
                                />
                            </div>
                            <div>
                                <input 
                                    bind:value={loginData.password}
                                    type="password"
                                    class="w-full px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20"
                                    placeholder="Şifre"
                                />
                            </div>
                            <button 
								on:click={handleLogin}
								disabled={loading}
								class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 disabled:from-gray-600 disabled:to-gray-700 text-white py-4 px-6 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl disabled:shadow-none"
							>
								{#if loading}
									<span class="flex items-center justify-center">
										<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
										Giriş yapılıyor...
									</span>
								{:else}
									Giriş Yap
								{/if}
							</button>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    {:else}
        <!-- Header -->
        <header class="sticky top-0 z-50 backdrop-blur-xl bg-black/40 border-b border-red-500/20">
            <div class="container mx-auto px-6 py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-black rounded-xl flex items-center justify-center shadow-lg">
                            <span class="text-lg font-black text-white">R</span>
                        </div>
                        <h1 class="text-2xl font-black bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent">@retto/social</h1>
                    </div>
                    
                    <div class="flex items-center space-x-4">
                        <div class="flex items-center space-x-3">
                            <select 
                                bind:value={timelineType}
                                on:change={loadTimeline}
                                class="px-4 py-2 rounded-xl bg-black/40 border border-red-500/20 text-white backdrop-blur-sm focus:ring-2 focus:ring-red-500/20 transition-all duration-300"
                            >
                                <option value="public">Tüm Gönderiler</option>
                                <option value="home">Benim Akışım</option>
                            </select>
                        </div>

                        <button 
                            on:click={toggleTheme}
                            class="p-3 rounded-xl bg-black/40 border border-red-500/20 backdrop-blur-sm hover:bg-red-500/20 transition-all duration-300 transform hover:scale-110"
                        >
                            {#if darkMode}
                                <span class="text-xl">☀️</span>
                            {:else}
                                <span class="text-xl">🌙</span>
                            {/if}
                        </button>

                        {#if user}
                            <div class="flex items-center space-x-3 bg-black/40 border border-red-500/20 rounded-xl px-4 py-2 backdrop-blur-sm">
                                <img src={user.avatar} alt={user.username} class="w-8 h-8 rounded-lg border-2 border-red-500/30" />
                                <span class="font-semibold text-white">@{user.username}</span>
                                <button 
                                    on:click={logout}
                                    class="ml-2 bg-red-600/80 hover:bg-red-500 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-300 hover:scale-105"
                                >
                                    Çıkış
                                </button>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            {#if errorMessage}
                <div class="max-w-2xl mx-auto mb-6 p-4 bg-red-500/20 border border-red-500/30 text-red-100 rounded-2xl backdrop-blur-sm">
                    <div class="flex items-center">
                        <div class="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center mr-3">
                            <span class="text-xs font-bold">!</span>
                        </div>
                        {errorMessage}
                    </div>
                </div>
            {/if}

            <!-- Yeni Gönderi Kutusu -->
            <div class="max-w-2xl mx-auto mb-8 p-6 rounded-3xl backdrop-blur-xl bg-white/10 dark:bg-black/20 border border-white/20 dark:border-red-500/20 shadow-2xl">
                <textarea 
                    bind:value={newPostContent}
                    placeholder="Dünyaya ne haber veriyorsun?"
                    class="w-full h-24 px-4 py-3 rounded-2xl bg-white/5 border border-white/10 focus:border-red-500/50 text-white placeholder-red-200/50 backdrop-blur-sm transition-all duration-300 focus:ring-2 focus:ring-red-500/20 resize-none"
                />
                <div class="flex justify-between items-center mt-4">
                    <span class="text-sm text-red-200/60">
                        {newPostContent.length}/500
                    </span>
                    <button 
						on:click={postStatus}
						disabled={loading || !newPostContent.trim()}
						class="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 disabled:from-gray-600 disabled:to-gray-700 text-white px-6 py-3 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg disabled:shadow-none"
					>
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

            <!-- Timeline -->
            <div class="max-w-2xl mx-auto">
                {#if loading && posts.length === 0}
                    <div class="text-center py-12">
                        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-black rounded-2xl mb-4 shadow-2xl animate-pulse">
                            <span class="text-2xl font-bold text-white">N</span>
                        </div>
                        <p class="text-red-200/60 mt-4">Gönderiler yükleniyor...</p>
                    </div>
                {:else if posts.length > 0}
                    <div class="space-y-6">
                        {#each posts as post}
                            <div class="rounded-3xl backdrop-blur-xl bg-white/10 dark:bg-black/20 border border-white/20 dark:border-red-500/20 shadow-2xl overflow-hidden transition-all duration-500 hover:border-red-500/40 hover:shadow-2xl">
                                <div class="p-6">
                                    <div class="flex items-start space-x-4">
                                        <img 
                                            src={post.account.avatar} 
                                            alt={post.account.username}
                                            class="w-12 h-12 rounded-xl border-2 border-red-500/30 shadow-lg"
                                        />
                                        <div class="flex-1 min-w-0">
                                            <div class="flex items-center space-x-3 mb-2">
                                                <span class="font-bold text-white text-lg">{post.account.display_name}</span>
                                                <span class="text-red-200/60 text-sm">@{post.account.username}</span>
                                                <span class="text-red-200/40 text-sm">•</span>
                                                <span class="text-red-200/40 text-sm">{formatDate(post.created_at)}</span>
                                            </div>
                                            <div class="prose prose-invert max-w-none">
												<div class="text-white/90 leading-relaxed">
													{@html post.content}
												</div>
											</div>
                                        </div>
                                    </div>

                                    {#if post.media_attachments.length > 0}
                                        <div class="mt-4 grid gap-2 {post.media_attachments.length === 1 ? 'grid-cols-1' : 'grid-cols-2'}">
                                            {#each post.media_attachments as media}
                                                {#if media.type === 'image'}
                                                    <img 
                                                        src={media.url} 
                                                        alt="Gönderi resmi"
                                                        class="rounded-2xl border border-white/10 shadow-lg hover:scale-105 transition-transform duration-300 cursor-zoom-in max-h-96 object-cover w-full"
                                                    />
                                                {/if}
                                            {/each}
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="text-center py-12">
                        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-black rounded-2xl mb-4 shadow-2xl">
                            <span class="text-2xl font-bold text-white">N</span>
                        </div>
                        <p class="text-red-200/60">Henüz gönderi yok</p>
                    </div>
                {/if}
            </div>
        </main>
    {/if}
</div>

<style>
    .prose {
        max-width: none;
    }
    .prose p {
        margin: 0;
        line-height: 1.6;
    }
    .prose a {
        color: #f87171;
        text-decoration: none;
    }
    .prose a:hover {
        color: #ef4444;
        text-decoration: underline;
    }
</style>