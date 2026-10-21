# Fantasy Hoops Lock-In Lab

## Free hosting and automatic schedule updates
1. Create a **public GitHub repository** and upload the contents of this folder (including `.github/workflows/refresh.yml`).
2. In repository **Settings → Pages**, choose **Deploy from a branch**, `main`, `/ (root)` and save.
3. In **Actions**, open **Refresh NBA data** and click **Run workflow** once. Scheduled runs are requested every 30 minutes, but GitHub may delay or disable them on inactive repositories.
4. If the action cannot push, go to **Settings → Actions → General → Workflow permissions** and choose **Read and write permissions**, then rerun. Repo policies may restrict this option.
5. Open the GitHub Pages URL displayed in Settings → Pages. The website will load `data/nba.json` when opened and periodically recheck it.

No API key or subscription is needed. ESPN endpoints are unofficial and may fail or change. The refresh workflow deliberately retains the previous cache on partial fetch failure. It currently refreshes **schedules only**, not injuries, box scores, projections, or actual Sleeper lock-ins. Browser-local roster data does not sync between devices. GitHub Pages is public; don't put private credentials in the repository.
