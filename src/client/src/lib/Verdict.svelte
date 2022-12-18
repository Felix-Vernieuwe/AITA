<script>
    export let verdict;

    const labels_verdict = {
        "not the asshole": "nta",
        "no assholes here": "nah",
        "everyone sucks": "esh",
        "asshole": "yta",
        "info": "info"
    }

    const display_verdict = {
        "nta": "Not the A-hole",
        "nah": "No A-holes here",
        "esh": "Everyone Sucks",
        "yta": "Asshole",
        "info": "INFO"
    }

    verdict = verdict.length > 4 ? labels_verdict[verdict] : verdict.toLowerCase();

</script>

<span class="post-flair post-{[verdict]}">
    {display_verdict[verdict]}
</span>

<style>
    .post-flair {
        padding: 4px 8px;
        border-radius: 50px;

        font-size: 12px;
        font-weight: 600;
        color: var(--text-complement-accent-color);
        font-family: Noto Sans, Arial, sans-serif;

        white-space: nowrap;
    }

    .post-yta {
        background-color: #b8001f;
    }

    .post-yta:hover {
        background-color: #c32741;
    }

    .post-nta, .post-nah {
        background-color: #7193ff;
    }

    .post-nta:hover, .post-nah:hover {
        background-color: #87a4ff;
    }

    .post-esh {
        background-color: #cc3600;
    }

    .post-esh:hover {
        background-color: #d45527;
    }

    .post-info {
        background-color: #ffd635;
        color: var(--text-faint-color);
    }

    .post-info:hover {
        background-color: #ffdc54;
    }

</style>