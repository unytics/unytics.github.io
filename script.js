document.addEventListener('DOMContentLoaded', () => {
    console.log('Unytics landing page loaded');

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
