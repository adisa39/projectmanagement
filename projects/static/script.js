// Toggle left menu functionality
const toggleLeftMenu = document.getElementById('toggleLeftMenu');
const mainContainer = document.getElementById('main-container');
const topNav = document.getElementById('top-nav');
const leftMenu = document.querySelector('.sidenav');

toggleLeftMenu.addEventListener('click', () => {
    leftMenu.classList.toggle('sidenav_toggle');
    if (window.innerWidth >= 768) { // Check if screen size is larger than or equal to 1024px
        if (leftMenu.classList.contains('sidenav_toggle')) {
            mainContainer.style.marginLeft = '0px';
            topNav.classList.replace('lg:left-60', 'left-3');
        } else {
            mainContainer.style.marginLeft = '220px';
            leftMenu.classList.replace('left-3', 'lg:left-60');
        }
    } else {
        if (leftMenu.classList.contains('sidenav_toggle')) {
            mainContainer.style.marginLeft = '0px';
            topNav.classList.replace('lg:left-60', 'left-3');
        } else {
            mainContainer.style.marginLeft = '220px';
            leftMenu.classList.replace('left-3', 'lg:left-60');
        }
    }
});

// Adjust layout on window resize
window.addEventListener('resize', () => {
    if (window.innerWidth < 768 && !leftMenu.classList.contains('sidenav_toggle')) {
        mainContainer.style.marginLeft = '0px';
    } else if (window.innerWidth >= 768 && !leftMenu.classList.contains('sidenav_toggle')) {
        mainContainer.style.marginLeft = '220px';
    }
});
