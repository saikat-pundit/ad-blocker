// hide_ads.js – hides sponsored/promoted ad units

function hideAds() {
  // Facebook: hide feed unit if its text contains "Sponsored"
  document.querySelectorAll('div[data-pagelet="FeedUnit"]').forEach(unit => {
    if (unit.textContent.includes('Sponsored')) {
      unit.style.display = 'none';
    }
  });

  // X (Twitter): hide tweet if its text includes "Promoted"
  document.querySelectorAll('article[data-testid="tweet"]').forEach(tweet => {
    if (tweet.textContent.includes('Promoted')) {
      tweet.style.display = 'none';
    }
  });
}

// Run once on page load
hideAds();

// Watch for dynamically loaded content (endless scroll)
const observer = new MutationObserver(() => {
  hideAds();
});
observer.observe(document.body || document.documentElement, {
  childList: true,
  subtree: true
});
