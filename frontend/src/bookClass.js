import Vue from 'vue'
import BookClass from './BookClass.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(BookClass)
}).$mount('#app')
