<script>
    import axios from "axios";
    import Gradient from "./Gradient.svelte";
    import Verdict from "./Verdict.svelte";

    export let body;

    let methods = ["BERT", "MNB", "Doc2Vec"];
    let method = methods[0];

    let analyzed = false;
    let sentiment = { nta: true, certainty: 0.5210935092349745 };
    $: sentiment.certainty = Math.round(sentiment.certainty * 10000) / 100;
    async function analyze() {
        if (body !== undefined) {
            const options = {
                params: { body, method },
                headers: { "content-type": "application/json" }
            }
            const data = await axios.get("http://127.0.0.1:5000/sentiment", options)
            sentiment = data.data;
            analyzed = true;
        }
    }
    $: method, analyze();

    function message(nta) {
        if (nta) return "not the asshole";
        else     return "the asshole";
    }
</script>

<div class="sentiment-analysis">
    <select class="select-method" bind:value={method}>
        {#each methods as method}
            <option value={method}>{ method }</option>
        {/each}
    </select>

    <div class="post">
        {#if analyzed}
            <div class="sentiment-body">
                {method} considers the OP of this post to be <Verdict verdict={sentiment.nta ? "nta" : "yta"}/> with
                <Gradient class="analysis-percentage" value={sentiment.certainty} text={sentiment.certainty + '%'}/> certainty
            </div>
        {/if}
    </div>
</div>

<style>
    .sentiment-analysis {
        display: flex;
        flex: 0;
        flex-direction: column;
        gap: 16px;
    }

    .select-method {
        width: min-content;

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

    .sentiment-body {
        color: var(--text-color);
    }

</style>