<script>
    import { onMount } from "svelte";
    import axios from "axios";

    import Loading from "./Loading.svelte";

    export let url;

    let method;
    let methods = ["BERT", "LexRank"];

    let loading = true;
    let summary = {
        post: "",
        yta: "",
        yta_count: 'x',
        nta: "",
        nta_count: 'x'
    };
    $: verdicts = [{ content: summary.yta, count: summary.yta_count, verdict: "YTA" },
                   { content: summary.nta, count: summary.nta_count, verdict: "NTA" }];
    function summarize()
    {
        loading = true;
        summary.yta_count = "x";
        summary.nta_count = "x";
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

    function percentage(count)
    {
        let total = summary.yta_count + summary.nta_count;
        return Math.round(count / total * 10000) / 100;
    }
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
    {#if !loading}
        <div class="grid grid-cols-2 gap-2">
            {#each verdicts as { content, count, verdict }}
                <div class="rounded-md bg-slate-900 border-2 border-slate-400">
                    {#if count !== 0}
                        <div class="p-2 border-b-2 border-slate-400">
                            { percentage(count) }% of commenters judged { verdict }
                        </div>
                        <div class="p-2">
                            { content }
                        </div>
                    {:else}
                        <div class="p-2">No commenters judged { verdict }</div>
                    {/if}
                </div>
            {/each}
        </div>
    {/if}
</div>