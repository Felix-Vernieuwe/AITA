<script>
    // Didn't have enough time to implement SvelteKit routing, so enjoy this hacky solution instead
    import { Router, Route, navigate } from "svelte-routing";


    import DarkmodeToggle from "./lib/DarkmodeToggle.svelte";
    import Analysis from "./lib/Analysis.svelte";
    import Judgement from "./lib/Judgement.svelte";
    import PostsOverview from "./lib/PostsOverview.svelte";
    import {onMount} from "svelte";

    export let url = "/posts/";
    let previousUrl = '';


    let darkmode = false;
    $: document.body.classList.toggle("dark-theme", darkmode);

    let input_field = null;

    let query = "";

    let fieldTerms = ["title", "body"];
    let fields = fieldTerms.reduce((object, term) => ({...object, [term]: false}), {});
    fields.title = true;

    onMount(() => {
        navigate(window.location.pathname);
        url = window.location.pathname;
    });
</script>

<Router bind:url={url} class="main-screen">
    <div class="top-column">
        <div class="title-bar" on:click={() => {
            navigate('/posts');
            url = '/posts';
        }}>
            r/<span class="title-bar-highlighted">A</span>m<span class="title-bar-highlighted">I</span><span
                class="title-bar-highlighted">T</span>he<span class="title-bar-highlighted">A</span>nalyser
        </div>
        <div class="search-bar">
            <form on:submit|preventDefault={(e) => {navigate(`/posts/${query}`)}}>
                <div class="search-input" on:click={() => input_field.focus()}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                         class="search-color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    >
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input bind:this={input_field} type="text" placeholder="Search for posts..."
                           bind:value={query}/>
                </div>

            </form>
            <div class="search-buttons">
                {#each Object.keys(fields) as field}
                    <button class="search-button" class:search-button-active={fields[field]}
                            on:click|preventDefault={() => fields[field] = !fields[field]}>
                        { field }
                    </button>
                {/each}
            </div>
        </div>
        <div class="top-right-bar">
            <button class="judge-button" on:click={() => {
                if (url === '/judge') {
                    history.back();
                    url = previousUrl || '/posts';
                } else {
                    navigate('/judge');
                    previousUrl = url;
                    url = '/judge'
                }
            }}>
                {url !== '/judge' ? "Judge Me!" : "Back"}
            </button>
            <DarkmodeToggle bind:darkmode/>
        </div>
    </div>
    <div class="bottom-column">
        <Route path="/posts/:query" let:params>
            <PostsOverview query={params.query}/>
        </Route>
        <Route path="/post/:id" let:params>
            <Analysis url={params.id}/>
        </Route>
        <Route path="/judge" component={Judgement}/>
    </div>
</Router>