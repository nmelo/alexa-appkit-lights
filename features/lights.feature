# Created by nmelo at 11/07/15
Feature: Toggle Power of Lifx bulbs

  Scenario: Turn off lights
    Given lights are on
    When we visit the control page
    Then turn lights off

  Scenario: Turn on lights
    Given lights are off
    When we visit the control page
    Then turn lights on
