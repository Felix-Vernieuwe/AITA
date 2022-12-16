<script>
    import { onMount } from "svelte";
    import axios from "axios";

    import Loading from "./Loading.svelte";

    export let url;

    let method;
    let methods = ["LexRank", "BERT"];

    let loading = true;
    let summary = {
        post: "",
        yta: "",
        yta_count: 0,
        nta: "",
        nta_count: 0
    };
    $: verdicts = [{ content: summary.yta, count: summary.yta_count, verdict: "YTA" },
                   { content: summary.nta, count: summary.nta_count, verdict: "NTA" }];
    function summarize()
    {
        loading = true;
        const options = {
            params: { url, method },
            headers: { "content-type": "application/json" }
        }
        axios.get("http://127.0.0.1:5000/summary", options)
            .then(data => {
                summary = data.data;
                loading = false;
            });
    }

    onMount(summarize);
</script>

<div class="my-2 space-y-2">
    <div>
        <button class="p-1.5 rounded-md text-slate-200 bg-sky-700" on:click={summarize}>
            Summarize this post
        </button>
        <select class="p-1.5 ml-1 h-fit rounded-md bg-sky-700 text-lg text-slate-200" bind:value={method}>
            {#each methods as method}
                <option value={method}>{ method }</option>
            {/each}
        </select>
    </div>
    <div class="p-2 rounded-md border-2 border-slate-400 bg-slate-900">
        {#if loading}
            <div class="my-4">
                <Loading></Loading>
            </div>
        {:else}
            { summary.post }
        {/if}
    </div>
    <div class="grid grid-cols-2 gap-2">
        {#each verdicts as { content, count, verdict }}
            <div class="rounded-md bg-slate-900 border-2 border-slate-400">
                <div class="p-2 border-b-2 border-slate-400">
                    { count } commenters judged { verdict }
                </div>
                <div class="p-2">
                    { content }
                </div>
            </div>
        {/each}
    </div>
</div>