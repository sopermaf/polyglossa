<template>
  <v-container>
    <v-layout wrap justify-center>
        <h1> About Us </h1>

        <div class="break" />

        <v-flex ma-5 lg3 xs6>
            <v-img
                class="framed"
                alt="conner pe profile photo"
                :src="profile_photo"
            >
            </v-img>
        </v-flex>

        <div class="break" />

        <v-flex ma-5 lg7 s12 xs12>
            <h2> Our Philosophy </h2>
            <p>
                Here at Polyglossa, we believe that everybody has the ability to
                speak English well, and we want to help students discover that ability!
                Primarily, we want to help students gain confidence in their pronunciation,
                their listening comprehension, and their use of native structures. We believe 
                that if students focus on these areas, they will see their English level increase
                dramatically. Our seminars are designed to help students practice these specific
                skills and develop their overall English fluency. Sign up for a seminar and
                start learning real English today!
            </p>
        </v-flex>

        <div class="break" />

        <v-flex ma-5 lg7 s12 xs12>
            <h2> Our Teacher </h2>
            <p>
                Conner is a TEFL-certified English teacher from San Diego, California. He has
                been teaching English for many years, and he holds a Bachelor’s Degree in
                English and Writing from Southern Oregon University. Throughout his career, he
                has taught in classrooms, businesses, language schools, tutoring centers, and on
                online platforms. Conner has had the opportunity to teach students from over 80 different
                countries and from many different linguistic backgrounds. Conner specializes in
                teaching pronunciation and listening comprehension by helping students improve
                their ability to identify the correct sounds and rhythm in English sentences. He
                also emphasizes the need for students to learn native grammatical structures, and
                he helps students incorporate these elements into their own speech. Conner’s passion
                for teaching English has also motivated him to study 4 different foreign languages himself,
                which has helped him better understand his students’ difficulties.
            </p>
        </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
      profile_photo: "https://lh3.googleusercontent.com/Gqq568MpQ-P9WyScZen-e4Wwf8gVn7Z0IIhq8yMp4p_Ch46z_wSjDxy9OmvFdyjOs_QjvsTPEB5oZ5VaZjhvOS8_vkQ7fUnNl85lGJZlFqZirQZdiKLennDNj1n1AiuBDGew8LXA_Q=w2400",
  }),
};
</script>

<style scoped>
    .framed {
        border: 3px solid black;
    }
</style>