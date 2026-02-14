// Run in browser console via evaluate
(() => {
  const links = Array.from(document.querySelectorAll('a[href*="/jobsearch/viewjob/"]'));
  return links.slice(0, 60).map(a => a.href);
})();
