#An IRC frontend for the wutwutwut?
##That's right, for the WWW
###That's the World Wide Web


##Why write a Web-based IRC frontend?
IRC is one of my favorite chat protocols. It's back to basics but powerful, and it's accessible via a wide variety of clients. However, lots of newbs don't even know about it because there aren't any good web clients. Until the advent of WebSockets, the only viable approach was shitty Java clients like Mibbit.

I wanted to include IRC as a part of my enclav.es project, so that the realtime chat clients present in each enclave would have a one-to-one relationship with an IRC channel on a private network. When a user creates an enclave, a channel will be registered with the to-exist ChanServ on my network, and when they chat in the browser, users in IRC will see what they say, and vice versa.

The first part of this is the wutwutwutirc client. This is a proof of concept client using Twisted to communicate with an IRC server and Tornado to provide websockets communication with the browser. It's realtime, it works. It accepts commands (/nick, /msg, and /kick) and obviously performs normal chat. Right now there's no way to change channels or networks; all that is hard-coded in, but it wouldn't be difficult to change that. I will, however, likely not bother since my goal is to integrate this into enclav.es and this is really just a proof of concept.

If you're looking to add an IRC frontend to your app this would be a good place to start or if you wish to add features to this one as a standalone client, however, if you submit a pull request I'll give you write access to the repo.
