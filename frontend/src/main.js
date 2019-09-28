import Vue from 'vue'
import Main from './Main.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(Main)
}).$mount('#app')
