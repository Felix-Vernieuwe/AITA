    <div class="spinner"/>


<style>
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .spinner {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;

        margin: auto;

        width: 40px;
        height: 40px;
        border: 6px solid #f3f3f3;
        border-top: 6px solid var(--primary-accent-color);
        border-radius: 50%;
        animation: spin 0.6s linear infinite;
    }
</style>