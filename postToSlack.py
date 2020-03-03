#coding: UTF-8

import slackweb

slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
slack.notify(text="pythonからslackさんへ")



