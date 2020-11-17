import Vue from 'vue'
import Payment from './Payment.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(Payment)
}).$mount('#app')
