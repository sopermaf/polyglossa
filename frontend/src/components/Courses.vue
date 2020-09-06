<template>
  <v-container>
    <v-layout text-center justify-center wrap>

      <v-flex mb-5 xs12>
        <h1> Seminars </h1>
      </v-flex>

      <v-flex ma-2 lg4 md4 sm4 xs6 v-for="sem in mockSeminars" :key="sem">
        <CourseSlot :sem="sem" @courseChoice="openForm"/>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import CourseSlot from "./CourseSlot";

export default {
  components: {
    CourseSlot,
  },
  props: {
    seminars: {
      type: Array,
      required: true,
    }
  },
  data: () => ({
    courseChoice: null,
    mockSeminars: [
      {title: 'Basic English', price: '3.80', description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ac lorem quis nisi porta egestas in id nisi. Suspendisse sit amet cursus leo. Sed blandit tincidunt nisl, at congue nibh vestibulum sit amet. Ut sagittis, ligula vulputate pulvinar convallis, metus purus ultricies urna, ut eleifend massa tellus mattis metus. Proin a est eget arcu vestibulum convallis a a risus. Vivamus ut massa nibh. Fusce convallis molestie libero pulvinar ultricies. Quisque vulputate eleifend libero vel ultrices. Nullam molestie quis nibh eget pellentesque. Aliquam faucibus euismod orci. Sed nec nunc felis. Suspendisse fermentum metus id ex sodales, ac pellentesque erat fermentum. In et metus at urna gravida semper gravida eget ex. Mauris quis blandit neque, in rutrum tellus. Mauris in mollis metus. Donec iaculis fermentum vulputate'},
      {title: 'Grammar Essentials', price: '25', description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ac lorem quis nisi porta egestas in id nisi. Suspendisse sit amet cursus leo. Sed blandit tincidunt nisl, at congue nibh vestibulum sit amet. Ut sagittis, ligula vulputate pulvinar convallis, metus purus ultricies urna, ut eleifend massa tellus mattis metus. Proin a est eget arcu vestibulum convallis a a risus. Vivamus ut massa nibh. Fusce convallis molestie libero pulvinar ultricies. Quisque vulputate eleifend libero vel ultrices. Nullam molestie quis nibh eget pellentesque. Aliquam faucibus euismod orci. Sed nec nunc felis. Suspendisse fermentum metus id ex sodales, ac pellentesque erat fermentum. In et metus at urna gravida semper gravida eget ex. Mauris quis blandit neque, in rutrum tellus. Mauris in mollis metus. Donec iaculis fermentum vulputate'},
      {title: 'Word of the Day', price: '2.50', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ac lorem quis nisi porta egestas in id nisi. Suspendisse sit amet cursus leo. Sed blandit tincidunt nisl, at congue nibh vestibulum sit amet. Ut sagittis, ligula vulputate pulvinar convallis, metus purus ultricies urna, ut eleifend massa tellus mattis metus. Proin a est eget arcu vestibulum convallis a a risus. Vivamus ut massa nibh. Fusce convallis molestie libero pulvinar ultricies. Quisque vulputate eleifend libero vel ultrices. Nullam molestie quis nibh eget pellentesque. Aliquam faucibus euismod orci. Sed nec nunc felis. Suspendisse fermentum metus id ex sodales, ac pellentesque erat fermentum. In et metus at urna gravida semper gravida eget ex. Mauris quis blandit neque, in rutrum tellus. Mauris in mollis metus. Donec iaculis fermentum vulputate'},
      {title: 'Colloquial English', price: '2.99', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ac lorem quis nisi porta egestas in id nisi. Suspendisse sit amet cursus leo. Sed blandit tincidunt nisl, at congue nibh vestibulum sit amet. Ut sagittis, ligula vulputate pulvinar convallis, metus purus ultricies urna, ut eleifend massa tellus mattis metus. Proin a est eget arcu vestibulum convallis a a risus. Vivamus ut massa nibh. Fusce convallis molestie libero pulvinar ultricies. Quisque vulputate eleifend libero vel ultrices. Nullam molestie quis nibh eget pellentesque. Aliquam faucibus euismod orci. Sed nec nunc felis. Suspendisse fermentum metus id ex sodales, ac pellentesque erat fermentum. In et metus at urna gravida semper gravida eget ex. Mauris quis blandit neque, in rutrum tellus. Mauris in mollis metus. Donec iaculis fermentum vulputate'},
    ]
  }),
  methods: {
    openForm(seminar) {
      this.$emit("courseChoice", seminar);
    }
  }
};
</script>
