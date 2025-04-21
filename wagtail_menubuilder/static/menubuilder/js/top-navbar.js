document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuButton = document.querySelector('.mobile-menu-button');
  const menu = document.getElementById('navbar-default');

  if (mobileMenuButton && menu) {
    mobileMenuButton.addEventListener('click', function () {
      const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
      menu.classList.toggle('active');
      mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
    });
  }
});