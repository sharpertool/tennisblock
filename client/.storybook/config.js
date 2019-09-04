import {addParameters, configure, addDecorator} from '@storybook/react'
import addonAPI from '@storybook/addons'
import {STORY_CHANGED} from '@storybook/core-events'

function loadStories() {
  const req = require.context('../stories', true, /\.stories\.js$/)
  req.keys().forEach(filename => req(filename))
}

addonAPI.register('sharpertool/config',
  storybookAPI => {
    storybookAPI.on(STORY_CHANGED, (kind, story) => console.log(kind, story))
  }
)

addParameters({
  options: {
    showPanel: true,
    panelPosition: 'bottom',
  }
})
configure(loadStories, module)
