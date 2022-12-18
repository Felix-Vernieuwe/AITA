<script>
    import Sentiment from "./Sentiment.svelte";
    import axios from "axios";
    import Verdict from "./Verdict.svelte";
    import Gradient from "./Gradient.svelte";

    let body;

    let methods = ["BERT", "MNB", "Doc2Vec"];
    let method = methods[0];
    let analyzed = false;
    let sentiment = { nta: true, certainty: 0.5210935092349745 };
    $: sentiment.certainty = Math.round(sentiment.certainty * 10000) / 100;

    async function analyze() {
        analyzed = false;
        if (body !== undefined) {
            const options = {
                params: {body, method},
                headers: {"content-type": "application/json"}
            }
            const data = await axios.get("http://127.0.0.1:5000/sentiment", options)
            sentiment = data.data;
            analyzed = true;
        }
    }
</script>


<div class="judgement">
    <textarea class="judgement-area" placeholder="Describe your grievings here..." bind:value={body}
        on:keyup={async (e) => {
            if (e.key === "Enter" && e.ctrlKey) {
                await analyze();
            }
        }}
    />
    <div class="input-fields">
        <select class="select-method" bind:value={method}>
            {#each methods as method}
                <option value={method}>{ method }</option>
            {/each}
        </select>
        <div class="judge-button">
            Judge!
        </div>
    </div>
    <div class="post verdict">
        {#if analyzed}
            <div class="sentiment-body">
                {method} considers the OP of this post to be
                <Verdict verdict={sentiment.nta ? "nta" : "yta"}/>
                with
                <Gradient class="analysis-percentage" value={sentiment.certainty} text={sentiment.certainty + '%'}/>
                certainty
            </div>
        {/if}
    </div>
</div>

<style>
    .judgement {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 16px;
    }

    .input-fields {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex: 0;
        gap: 16px;
    }

    .judgement-area {
        border-radius: 16px;
        margin: 16px;
        padding: 16px;
        outline: 1px solid var(--border-color);
        resize: none;

        height: 500px;
        width: 700px;

        font-family: IBM Plex Sans, Arial, sans-serif;
        font-size: 16px;

    }

    .judgement-area:focus {
        outline: 2px solid var(--border-color-hover);
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


    .judge-button {
        margin: 0 8px;
        padding: 8px 16px;
        border-radius: 20px;

        font-family: Noto Sans, Arial, sans-serif;
        font-size: 14px;
        font-weight: 700;

        cursor: pointer;
        border: 0;
        background-color: var(--secondary-accent-color);
        color: var(--text-complement-accent-color);
        transition: background-color 0.2s ease-in-out;
    }

    .judge-button:hover {
        background-color: var(--secondary-accent-color-hover);
    }



    .verdict {
        min-width: 700px;
        min-height: 30px;
        text-align: center;
    }

</style>
