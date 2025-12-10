document.addEventListener('DOMContentLoaded', () => {
    // Language detection and switching
    const STORAGE_KEY = 'unytics_language_preference';
    const currentLang = document.documentElement.lang || 'en';

    // Toast messages by language
    const toastMessages = {
        en: "Email copied to clipboard!",
        fr: "Email copié dans le presse-papier !"
    };

    function getBrowserLanguage() {
        const browserLang = navigator.language || navigator.userLanguage;
        return browserLang.split('-')[0].toLowerCase();
    }

    function getStoredLanguage() {
        return localStorage.getItem(STORAGE_KEY);
    }

    function storeLanguage(lang) {
        localStorage.setItem(STORAGE_KEY, lang);
    }

    function getLanguageUrl(targetLang) {
        const currentHash = window.location.hash;

        if (targetLang === 'fr') {
            if (currentLang === 'en') {
                return '/fr/' + currentHash;
            }
        } else if (targetLang === 'en') {
            if (currentLang === 'fr') {
                return '/' + currentHash;
            }
        }

        return null;
    }

    function autoDetectLanguage() {
        const storedLang = getStoredLanguage();
        const browserLang = getBrowserLanguage();

        // Priority: stored preference > browser language
        const preferredLang = storedLang || browserLang;

        // If preferred language doesn't match current page, redirect
        if (preferredLang !== currentLang) {
            const targetUrl = getLanguageUrl(preferredLang);
            if (targetUrl) {
                storeLanguage(preferredLang);
                window.location.href = targetUrl;
            }
        } else {
            // Always store the current language as preference
            storeLanguage(currentLang);
        }
    }

    function initLanguageSwitcher() {
        const langButtons = document.querySelectorAll('.lang-btn');

        langButtons.forEach(btn => {
            const btnLang = btn.getAttribute('data-lang');

            if (btnLang === currentLang) {
                btn.classList.add('active');
            }

            btn.addEventListener('click', () => {
                const targetLang = btn.getAttribute('data-lang');

                // Always store the language preference when user clicks
                storeLanguage(targetLang);

                const targetUrl = getLanguageUrl(targetLang);
                if (targetUrl) {
                    window.location.href = targetUrl;
                }
            });
        });
    }

    // Run auto-detection FIRST (before DOM manipulation)
    autoDetectLanguage();

    // Then initialize language switcher buttons
    initLanguageSwitcher();

    // Mobile menu toggle implementation
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.flexDirection = 'column';
                navLinks.style.backgroundColor = 'white';
                navLinks.style.padding = '1rem';
                navLinks.style.boxShadow = '0 4px 6px -1px rgba(0,0,0,0.1)';
            } else {
                navLinks.style = '';
            }
        });

        // Close mobile menu when clicking a menu item
        const menuItems = navLinks.querySelectorAll('a');
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.style.display = 'none';
                navLinks.style = '';
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navLinks.style.display === 'flex' && !navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
                navLinks.style.display = 'none';
                navLinks.style = '';
            }
        });
    }

    // Accordion functionality
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const accordionItem = header.parentElement;
            const isActive = accordionItem.classList.contains('active');

            // Close all accordion items
            document.querySelectorAll('.accordion-item').forEach(item => {
                item.classList.remove('active');
            });

            // Toggle current item
            if (!isActive) {
                accordionItem.classList.add('active');
            }
        });
    });

    // Copy email to clipboard functionality
    const copyEmailLinks = document.querySelectorAll('.copy-email');
    const toast = document.getElementById('toast');

    copyEmailLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const email = link.getAttribute('data-email');

            // Copy to clipboard
            navigator.clipboard.writeText(email).then(() => {
                // Set toast message based on current language
                toast.textContent = toastMessages[currentLang] || toastMessages.en;

                // Show toast notification
                toast.classList.add('show');

                // Hide toast after 3 seconds
                setTimeout(() => {
                    toast.classList.remove('show');
                }, 3000);
            }).catch(err => {
                console.error('Failed to copy email: ', err);
            });
        });
    });
});
