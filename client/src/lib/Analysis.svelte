<script>
    import { onMount } from "svelte";
    import axios from "axios";

    import Loading from "./Loading.svelte";

    export let url;
    let fullUrl = `https://www.reddit.com/r/AmItheAsshole/comments/${url}`

    let loading = true;
    let post = { comments: [], body: "", title: "" };
    onMount(() => {
        const options = {
            params: { url },
            headers: { "content-type": "application/json" }
        }
        axios.get("http://127.0.0.1:5000/post", options)
            .then(data => {
                loading = false;
                post = data.data;
                console.log(post.comments.length);
            });
    });
</script>

{#if loading}
    <Loading/>
{:else}
    <div class="p-2 h-full grid grid-cols-2 gap-2">
        <div>
            <div class="h-96 bg-slate-900 relative rounded-md border-2 border-slate-400 overflow-scroll">
                <div class="p-2 bg-inherit sticky top-0 border-b-2 border-slate-400 text-xl">
                    { post.title }
                </div>
                <div class="p-2">
                    {@html post.body }
                </div>
            </div>
            <div class="my-2 p-2 w-fit h-fit rounded-md bg-sky-700 text-slate-200">
                <a href={fullUrl} target="_blank" rel="noreferrer">
                    See original post
                </a>
            </div>
        </div>
        <div class="overflow-scroll space-y-2">
            {#each post.comments as comment}
                <div class="p-2 bg-slate-900 rounded-md border-2 border-slate-400">
                    {@html comment}
                </div>
            {/each}
        </div>
    </div>
{/if}