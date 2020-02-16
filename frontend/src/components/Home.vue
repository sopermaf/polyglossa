<template>
  <v-container>
    <v-layout text-center wrap>
      <v-img
          :src="require('../assets/polyglossa_logo.png')"
          class="my-3"
          contain
          height="200"
        ></v-img>

      <v-flex mt-5 mb-5 xs12>
        <v-layout justify-center>
          Flexible Online Language Classes and Resources
        </v-layout>
      </v-flex>

      <v-flex mb-5 xs12>
        <h3 class="display-1 font-weight-light mb-3">
          <span>Learn English</span>
          <span class="font-weight-bold">
            Your
          </span>
          <span>Way</span>
        </h3>
      </v-flex>

      <v-flex mb-5 xs12>
        <v-layout justify-center>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus a nulla molestie, congue neque ut,
            accumsan sapien. Nullam vestibulum est sed turpis consequat iaculis.
            Sed semper vel tellus id varius. In ac lectus vel sem posuere porttitor sit amet quis lectus. Duis
            tristique, nisl ut ullamcorper convallis, augue nisi elementum nibh, faucibus venenatis urna dui vitae dolor.
            Quisque finibus sodales sem, vel pharetra enim. Ut sed magna maximus, feugiat massa eget, commodo ante.
            Suspendisse potenti. Integer convallis mattis augue eu cursus. Sed et lacinia quam. Nunc vel neque 
            justo. Sed blandit, justo sed tempor euismod, tortor erat euismod felis, ut blandit nisl urna non massa.
             Mauris lorem risus, interdum vel lorem at, semper efficitur dolor. Maecenas eu semper ex. Ut pretium erat
              nec aliquam fringilla.
          </p>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    classTypes: [
      {
        text: 'Personalised Class',
        href: 'https://vuetifyjs.com/components/api-explorer',
      },
      {
        text: '$2 Live Classes',
        href: 'https://vuetifyjs.com/layout/pre-defined',
      },
      {
        text: 'PolyProgram',
        href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
      },
      {
        text: 'Try an Experimental Class',
        href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
      },
    ],
  }),
};
</script>
