// Shared behavior for all pages
function toggleMenu() {
    document.getElementById('hamburger').classList.toggle('active');
    document.getElementById('mobileMenu').classList.toggle('open');
    document.getElementById('mobileBackdrop').classList.toggle('open');
}

// Page fade transition (leaves ctrl/cmd/middle-click alone)
window.addEventListener('pageshow', () => document.body.classList.remove('fade-out'));

document.querySelectorAll('a[href$=".html"]:not(.order-button)').forEach(link => {
    link.addEventListener('click', function(e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
        e.preventDefault();
        const href = this.getAttribute('href');
        document.body.classList.add('fade-out');
        setTimeout(() => { window.location.href = href; }, 500);
    });
});
