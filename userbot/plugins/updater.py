"""Update UserBot Code (FOR MEGASTAR UB)
Syntax: .update
\nAll Credits goes to © MEGASTAR UB
\nFor this awasome plugin.\nPorted from PpaperPlane Extended"""
import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP
from userbot.utils import admin_cmd

UPSTREAM_REPO_URL = environ.get(
    "GITHUB_REPO_URL", "https://github.com/Bristi-OP/MEGASTAR"
)
HEROKU_API_KEY = Var.HEROKU_API_KEY
HEROKU_APP_NAME = Var.HEROKU_APP_NAME

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "**Update Sucessfull, Please give me some time to restart the bot..**"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"༒[{c.committed_datetime.strftime(d_form)}]: {c.summary} by ʚ{c.author}ɞ\n"
        )
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@borg.on(admin_cmd(pattern="update ?(.*)", outgoing=True))
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
    conf = ups.pattern_match.group(1)
    await ups.edit("Checking for updates, please wait....")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "Oops.. Updater cannot continue due to "
        txt += "some problems occured\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f"{txt}\ndirectory {error} is not found")
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f"{txt}\nEarly failure! {error}")
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        if conf is None or conf == "":
            await ups.edit(
                f"𝗕𝗢𝗦𝗦!!!😉😉\nIt doesn't seem like a git repository. So I can't generate changelog. To get the Latest update of Megastar userbot type .update now 😏😏 "
            )
        return
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await ups.edit(
            f"**[UPDATER]:** Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if not changelog and not force_update and conf != "deploy":
        await ups.edit(f"\n**Your bot is up-to-date.**\n")
        repo.__del__()
        return
    if conf != "now":
        changelog_str = (
            f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n{changelog}"
        )
        if len(changelog_str) > 4096:
            await ups.edit("Changelog is too big, view the file to see it.")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond("do .update now to update")
        return
    if conf == "now":
        await ups.edit("**Just wait for a minute....**")
        await update(ups, repo, ups_rem, ac_br)
    return
    if force_update:
        await ups.edit(
            "༒**Megastar is being updated now**༒..\n**please wait Boss just wait for some minutes... Ill be up in time** 😉 "
        )
    else:
        await ups.edit("Updating userbot, please wait....you are my best boss ever 🤩🥳")
    if conf != "deploy":
        return
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await ups.edit(
                "Please set up the HEROKU_APP_NAME variable to be able to update userbot."
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f"{txt}\nInvalid Heroku credentials for updating userbot dyno."
            )
            repo.__del__()
            return
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
            await ups.edit("⬛⬛⬛⬛ \n⬛✳️✳️⬛ \n⬛✳️✳️⬛ \n⬛⬛⬛⬛")
            await asyncio.sleep(1)
            await ups.edit("⬛⬛⬛⬛ \n⬛🔴🔴⬛ \n⬛🔴🔴⬛ \n⬛⬛⬛⬛")
            await asyncio.sleep(1)
            await ups.edit("⬛⬛⬛⬛ \n⬛🌕🌕⬛ \n⬛🌕🌕⬛ \n⬛⬛⬛⬛")
            await asyncio.sleep(1)
            await ups.edit("⬛⬛⬛⬛ \n⬛🔵🔵⬛ \n⬛🔵🔵⬛ \n⬛⬛⬛⬛")
            await asyncio.sleep(1)
            await ups.edit("⬛⬛⬛⬛ \n⬛❇️❇️⬛ \n⬛❇️❇️⬛ \n⬛⬛⬛⬛")
            await asyncio.sleep(1)
        await ups.edit(
            "**༒𝚄𝙿𝙳𝙰𝚃𝙸𝙽𝙶 𝙼𝙴𝙶𝙰𝚂𝚃𝙰𝚁 𝚄𝚂𝙴𝚁𝙱𝙾𝚃༒\nBoss!!Please wait 5 minutes 😁😁\nThen try**  .alive **to check if I'm tuned.. 😎😎\n\nPowered by :-\n[MEGASTAR UB](https://t.me/MEGASTAR_SUPPORT)**"
        )
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await ups.edit(
            "Successfully Updated!\n" "Bot is restarting... Wait for a second!"
        )
        # Spin a new instance of bot
        args = [sys.executable, "-m", "userbot"]
        execle(sys.executable, *args, environ)
        return


CMD_HELP.update(
    {
        "updater": ".update\
\nUsage: Checks if the main userbot repository has any updates and shows a changelog if so.\
\n\n.update now\
\nUsage: Updates your userbot, if there are any updates in the main userbot repository."
    }
)
