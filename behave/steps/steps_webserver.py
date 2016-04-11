
from behave import *
import mechanize
import re

def escape_special_chars(s):
    return re.sub(r"([^a-zA-Z0-9_-])", lambda m: "\\%02X" % ord(m.group(1)), s)

@when(u"I access {url} as {user}/{password}")
def step_impl(context, url, user, password):
    br = mechanize.Browser()
    br.add_password(url, user, password)
    step_impl_download(context, url, br)

@when(u"I access {url}")
def step_impl_download(context, url, br=None):
    if br is None:
        br = mechanize.Browser()
    br.set_handle_robots(False)
    try:
        fp = br.open(url)
    except Exception, e:
        fp = e

    context.http_status_code = fp.code
    context.page_source = fp.read().decode("utf-8")

@then(u'the page will contain "{text}"')
@then(u"the page will contain '{text}'")
def step_impl(context, text):
    print(context.page_source)
    assert context.page_source.find(text) >= 0, "page source (%d bytes) didn't contain text '%s'" % (len(context.page_source), text)

@then(u'the page content will be "{text}"')
@then(u'the page content will be \'{text}\'')
def step_impl(context, text):
    text = text.replace("\\n", "\n")
    print("expected: " + escape_special_chars(text))
    print("received: " + escape_special_chars(context.page_source))
    assert context.page_source == text, "page source (%d bytes) was not '%s'" % (len(context.page_source), text)

@then(u'the status code will be {http_status_code}')
def step_impl(context, http_status_code):
    assert context.http_status_code == int(http_status_code), "HTTP code is '%d' but should be '%s'" % (context.http_status_code, http_status_code)
