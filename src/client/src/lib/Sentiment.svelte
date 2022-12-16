<script>
    export let sentiment;

    let asshole;
    if (sentiment.nta) asshole = "not the asshole";
    else               asshole = "the asshole";
</script>

<div class="p-1.5 text-right text-lg">
    Our AI model considers the OP of this post to be { asshole }, with { sentiment.certainty }% certainty
</div>