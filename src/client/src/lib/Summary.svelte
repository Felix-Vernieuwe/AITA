<script>
    import Gradient from "./Gradient.svelte";
    import axios from "axios";

    import Loading from "./Loading.svelte";

    export let url;

    let methods = ["BERT", "LexRank"];
    let method = methods[1];

    let loading = true;
    let summary = {
        post: "",
        yta: "",
        yta_count: 'x',
        nta: "",
        nta_count: 'x'
    };
    $: verdicts = [{content: summary.yta, count: summary.yta_count, verdict: "YTA"},
        {content: summary.nta, count: summary.nta_count, verdict: "NTA"}];

    function summarize() {
        loading = true;
        summary.yta_count = "x";
        summary.nta_count = "x";
        const options = {
            params: {url, method},
            headers: {"content-type": "application/json"}
        }
        axios.get("http://127.0.0.1:5000/summary", options)
            .then(data => {
                summary = data.data;
                loading = false;
            });
    }

    $: method, summarize();

    function percentage(count) {
        let total = summary.yta_count + summary.nta_count;
        return Math.round(count / total * 10000) / 100;
    }
</script>

<div class="analysis">
    <div>
        <select class="select-method" bind:value={method}>
            {#each methods as method}
                <option value={method}>{ method }</option>
            {/each}
        </select>
    </div>
    <div class="post summary-content">
        <p class="summary-title">Post summary</p>
        {#if loading}
            <Loading/>
        {:else}
            <p class="summary-body">
                { summary.post }
            </p>
        {/if}
    </div>
    {#if loading}
        <div class="post comment-verdict">
            <Loading/>
        </div>
        <div class="post comment-verdict">
            <Loading/>
        </div>
    {:else}
        {#each verdicts as {content, count, verdict}}
            <div class="post comment-verdict">
                {#if count !== 0}
                    <div class="comments-verdict-title">
                        <Gradient class="analysis-percentage" value={percentage(count)}
                                  text={percentage(count)+'%'}/>
                        of commenters judged <b>{ verdict }</b>
                    </div>
                    <div class="comments-verdict-body">
                        <b>Summary: </b>{ content }
                    </div>
                {:else}
                    <div class="comments-verdict-title">No commenters judged <b>{ verdict }</b></div>
                {/if}
            </div>
        {/each}
    {/if}
</div>

<style>
    .analysis {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .summary-content {
        min-height: 94px;
    }

    .summary-title {
        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 16px;
        font-weight: 600;
        margin-block-end: 0;
        color: var(--text-color);
    }

    .comments-verdict-title {
        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 6px;
        color: var(--text-color);
    }

    .summary-body {
        font-family: Noto Sans, Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: var(--text-faint-color);
    }

    .comments-verdict-body {
        font-family: Noto Sans, Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: var(--text-faint-color);
    }

    .select-method {
        height: 40px;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        background-color: var(--secondary-background);
        color: var(--text-color);
        font-family: IBM Plex Sans Medium, Arial, sans-serif;
        font-size: 16px;
        font-weight: 500;
        padding: 0 16px;
    }

    .comment-verdict {
        min-height: 100px;
    }

</style>