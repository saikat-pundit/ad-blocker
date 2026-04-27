// hide_ads.js – hides sponsored/promoted ad units

function hideAds() {
  // Facebook: hide feed unit if it contains a "Sponsored" link
  document.querySelectorAll('div[data-pagelet="FeedUnit"] a[aria-label="Sponsored"]').forEach(link => {
    const unit = link.closest('div[data-pagelet="FeedUnit"]');
    if (unit) unit.style.display = 'none';
  });

  // X / Twitter: hide tweet if its text includes "Promoted"
  document.querySelectorAll('article[data-testid="tweet"]').forEach(tweet => {
    if (tweet.textContent.includes('Promoted')) {
      tweet.style.display = 'none';
    }
  });
}

// Run once on page load
hideAds();

// Keep watching for dynamically loaded content (scrolling)
const observer = new MutationObserver(() => {
  hideAds();
});
observer.observe(document.body || document.documentElement, {
  childList: true,
  subtree: true
});
