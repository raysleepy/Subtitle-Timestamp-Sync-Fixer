# Subtitle Timestamp Sync Fixer

# Why
Have you ever tried to watch something in a foreign language with subtitle and realized that the subtitle is out of sync?

Have you ever wished that the subtitle will stay on the screen for a bit longer, so that you can read everything?

# How
Obviously, I can't fix Netflix/Amazon/Youtube and whatnot.

My solution is to download the video and subtitle and watch it offline with VLC Media Player.

How exactly you would do that is out of scope of this.
What's needed is a video file (e.g., mp4) and a SEPARATE srt (subtitle) file.

(You can use SubRip if you need to..)

VLC does have a built-in capability to adjust the synchronization of subtitle, relatie to the video.
However, doing that everytime for every video seems a bit painful.

And more importantly, It doesn't have the "stretching" capability.

This is a simple python script to fix that. You can wrap it in another script to do batch processing.
But in all honesty, each subtitle could be out of sync with a different amount of time.

But if the goal is to make the subtitle stay on the screen for a second or two longer, then, yes, you can totally do that in a batch process.

SRT file has simple format like this. Details are explained here:
https://docs.fileformat.com/video/srt/

# Usage Examples

```
% cat movie.srt
1
00:05:00,400 --> 00:05:15,300
This is an example of
a subtitle.

2
00:05:16,400 --> 00:05:25,300
This is an example of
a subtitle - 2nd subtitle.

% python subtitle-fixer.py movie.srt 1000 0 
INFO: movie.srt => movie.srt.org

% cat movie.srt
1
00:05:01,400 --> 00:05:16,300
This is an example of
a subtitle.

2
00:05:17,400 --> 00:05:26,300
This is an example of
a subtitle - 2nd subtitle.
```

Subtitle file "movie.srt" is saved to "movies.srt.org" and the new "movie.srt" created will delay the subtitle for one second (1000 ms).

```
%python subtitle-fixer.py movie.srt -1000 2500

% cat movie.srt                                
1
00:04:59,400 --> 00:05:16,800
This is an example of
a subtitle.

2
00:05:15,400 --> 00:05:26,800
This is an example of
a subtitle - 2nd subtitle.
```

Subtitle file "movie.srt" will be updated will to have the subtitle start one second (-1000 ms) earlier and stay on the screen for 2 seconds (2500 ms) longer than originally stated.

# NB
Timing adjustment is relative to the original file (movie.srt.org) - hence the reason for first saving the original SRT file.
The idea is that you may need to try a few times to get the timing adjustment to your liking.
