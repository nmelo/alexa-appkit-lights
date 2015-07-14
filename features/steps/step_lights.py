# -*- coding: UTF-8 -*-
"""
Toggle power
"""

# @mark.steps_lights
# ----------------------------------------------------------------------------
# STEPS: Toggle Power of Lifx bulbs
# ----------------------------------------------------------------------------
from behave import given, when, then


@given('lights are on')
def given_lights_on(context):
    pass


@given('lights are off')
def given_lights_off(context):
    pass


@when('we visit the control page')
def when_control(context):
    assert True is not False

    context.browser.get('http://www.google.com')


@then('turn lights on')
def then_turn_on(context):
    assert context.failed is False


@then('turn lights off')
def then_turn_off(context):
    assert context.failed is False

