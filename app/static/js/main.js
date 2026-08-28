document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        document.documentElement.setAttribute('data-theme', storedTheme);
    } else if (prefersDarkScheme.matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }

    if (themeToggleBtn) {
        updateToggleText();
        themeToggleBtn.addEventListener('click', () => {
            let currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateToggleText();
        });
    }

    function updateToggleText() {
        if (!themeToggleBtn) return;
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            themeToggleBtn.innerHTML = '<span>🌙 Dark Mode</span>';
            themeToggleBtn.setAttribute('aria-label', 'Current theme: dark. Click to switch theme.');
        } else {
            themeToggleBtn.innerHTML = '<span>☀️ Light Mode</span>';
            themeToggleBtn.setAttribute('aria-label', 'Current theme: light. Click to switch theme.');
        }
    }
});
