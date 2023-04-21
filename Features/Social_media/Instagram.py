import webbrowser

import instaloader
from Body.Speaker import Speak

Insta_acc = {
    "anish": "anishbochare_96k",
    "harshal": "__harshal.__12",
    "mayur": "maayu_r",
    "goku": "athrav_1912",
    "arpan": "arpan_patil11",
    "ajay": "a.karagir",
    "didi": "anushreee.dhore",
    "yogesh": "yjg87"
}


def profile(Insta_ID, person):
    bot = instaloader.Instaloader()
    profile_name = instaloader.Profile.from_username(bot.context, Insta_ID)
    username = profile_name.full_name
    number_of_post = profile_name.mediacount
    insta_followers = profile_name.followers
    insta_followings = profile_name.followees
    insta_boi = profile_name.biography
    Insta_Web = profile_name.profile_pic_url
    try:
        Speak(
            f"Sir Here are the Details of {username} Instagram Profile \nNumber of Posts: {number_of_post},\nFollowers: {insta_followers},\nFollowings: {insta_followings},\nBio: {insta_boi} and Your Profile Pic")
        webbrowser.open(Insta_Web)
    except instaloader.ProfileNotExistsException:
        print("Sir, The Username is i valid or there is an problem with your network")


def profile_info(ID_names):
    acc_id = str(ID_names).lower()
    insta_id = list(Insta_acc.keys())
    for insta_acc in insta_id:
        try:
            if insta_acc in acc_id:
                instagram_id = f"{Insta_acc[insta_acc]}"
                person_name = insta_acc
                profile(instagram_id, person_name)
                break
        except:
            pass
