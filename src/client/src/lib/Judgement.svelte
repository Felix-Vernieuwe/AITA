<script>
    import Sentiment from "./Sentiment.svelte";

    let body;
    let analyse;
</script>

<div>
    <textarea class="mt-2 p-2 w-full h-96 focus:outline-none focus:ring focus:ring-slate-400
                    resize-none rounded-md bg-slate-900 text-slate-400"
            placeholder="Describe your torments here..." bind:value={body}></textarea>
    <Sentiment bind:analyse {body}>Judge me!</Sentiment>
</div>