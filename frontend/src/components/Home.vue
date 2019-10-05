<template>
  <v-container>
    <v-layout
      text-center
      wrap
    >
      <!--<v-flex xs12>
        <v-img
          :src="require('../assets/polyglossa_logo.png')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex>-->

      <v-flex mt-5 mb-5 xs12>
        Flexible Online Language Classes and Resources
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
        <h2 class="headline font-weight-bold mb-3">Our Classes</h2>

        <v-layout justify-center>
          <a
            v-for="(next, i) in classTypes"
            :key="i"
            :href="next.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ next.text }}
          </a>
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
