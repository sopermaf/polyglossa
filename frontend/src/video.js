import Vue from 'vue'
import Video from './Video.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(Video)
}).$mount('#app')
