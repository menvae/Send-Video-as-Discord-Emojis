# What is this?
### `Send Video as Discord Emoji` allows you to take any video and send it as emojis
> Due to Discord rate limits it's adviced to encode the video in at most 5 - 10 fps if you're going to be sending it in real-time.
#
***
# Getting Started
## How to use
#### Head to [Releases](https://github.com/menvae/Send-Video-as-Discord-Emojis/releases) to download.

if you're using python install `requirements.txt` with pip:
```
pip install -r requirements.txt
```
##### Paste your Discord Bot token inside `token.txt`

> You can also use your user token but it is against [Discord's Guidelines](https://discord.com/guidelines/#:~:text=14.%20Do%20not%20use%20self%2Dbots%20or%20user%2Dbots.%20Each%20account%20must%20be%20associated%20with%20a%20human%2C%20not%20a%20bot.%20(See%20our%20Platform%20Manipulation%20Policy%20Explainer%20for%20more.)) and I'm not responible if discord takes action.


## Sending Messages

#### Run `Sender.exe`  or `main.py`
![main_window](https://github.com/menvae/Send-Video-as-Discord-Emojis/assets/116231436/585542b0-6c7e-4776-b981-4338b144773c)


#### **.vtd File**
Don't have a .vtd file? you can encode your own. Check out [Encoding](#encoding).

#### **Channel ID and Message ID**
If you don't know how to get the Channel ID and Message ID:
Go to **Discord > User Settings > Advanced**
and turn on **Developer Mode** , you can then right click on messages and channels to copy their ID.


<a name="encoding" />

## Encoding (.vtd files)
> To encode files you need to have ffmpeg installed and added to path otherwise, you won't be able to encode!

If you don't have a .vtd file, don't worry as you can turn any video into emojis.
#### Run `Encoder.exe`  or `encoder.py`
![encoder_window](https://github.com/menvae/Send-Video-as-Discord-Emojis/assets/116231436/09ed1573-819d-4a31-874b-c05f4f742464)


All options are here self-explainatory
> Encoding with high dimensions and a higher fps than 30 will be **heavy**.

###### not fun-fact: vtd stands for "Video To Discord"... wow who would've known...


# Showcase
![video to emoji showcase](https://github.com/menvae/Send-Video-as-Discord-Emojis/assets/116231436/bf36da11-84bc-4206-b35f-9e77a5b7a23f)


#
### Please report an issue if encountered
