import '@storybook/addon-viewport/register'
import '@storybook/addon-actions/register'
import '@storybook/addon-knobs/register'
import 'storybook-addon-redux-listener/register'
import addons from '@storybook/addons'
import registerRedux from 'addon-redux/register'
registerRedux(addons)
