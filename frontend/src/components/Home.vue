<template>
  <v-container>
    <v-layout text-center wrap justify-center>

      <v-flex ma-5 lg12 xs12>
        <h3 class="display-1 font-weight-light mb-3">
          <span>Learn</span>
          <span class="font-weight-bold font-italic">
            Real
          </span>
          <span>English</span>
        </h3>
      </v-flex>

      <div class="break" />

      <v-flex lg7 md8 sm10 xs12 >
          <p>
            Do you want to speak English
            <span class="font-weight-bold">fluently</span>
            and
            <span class="font-weight-bold">confidently</span>
            ?
            Do you want to improve your listening and pronunciation?

            Here at Polyglossa, our mission is to help you do exactly
            that!
            We want to help you speak English the way Americans really speak.
            In our English seminars, you will learn how to:
          </p>
      </v-flex>
      
      <div class="break" />

      <v-flex ma-2 lg2 md4 sm2 xs5 text-left>
          <ul>
            <li class="font-weight-bold">
              increase your fluency
            </li>
            <li class="font-weight-bold">
              improve your listening skills
            </li>
          </ul>
      </v-flex>

      <v-flex ma-2 lg3 md5 sm3 xs6 text-left>
          <ul>
            <li class="font-weight-bold">
              speak with correct pronunciation
            </li>
            <li class="font-weight-bold">
              use native expressions
            </li>
          </ul>
      </v-flex>

      <div class="break" />

      <v-flex lg7 md8 sm10 xs12 ma-5>
          <p>
            If you want to speak English better and understand more, join one of our seminars today!
          </p>
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
