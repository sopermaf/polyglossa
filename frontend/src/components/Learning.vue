<template>
  <v-container>
    <v-layout text-center wrap justify-center>
        <h1> Learning Materials </h1>
        <div class="break" />

        <v-tabs
            v-model="tab"
            color="primary"
            fixed-tabs
        >
            <v-tab
                v-for="level in learingMaterials"
                :key="level.title"
            >
                {{level.title}}
            </v-tab>
        </v-tabs>

        <v-tab-items
            v-model="tab"
        >
            <v-tab-item
                v-for="level in learingMaterials"
                :key="level.title"
            >
                {{level.title}}
            </v-tab-item>
        </v-tab-items>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    tab: null,
    learingMaterials: [
        {
            title: "A1",
            exerciseLinks: [
                "test",
                "test",
                "test",
            ],
            videoLinks: [
                "test",
                "test",
                "test",
            ],
            pdfLink: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "A2",
            exerciseLinks: [
                "test",
                "test",
                "test",
            ],
            videoLinks: [
                "test",
                "test",
                "test",
            ],
            pdfLink: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "B1",
            exerciseLinks: [
                "test",
                "test",
                "test",
            ],
            videoLinks: [
                "test",
                "test",
                "test",
            ],
            pdfLink: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "B2",
            exerciseLinks: [
                "test",
                "test",
                "test",
            ],
            videoLinks: [
                "test",
                "test",
                "test",
            ],
            pdfLink: [
                "test",
                "test",
                "test",
            ],
        },
        {
            title: "C1",
            exerciseLinks: [
                "test",
                "test",
                "test",
            ],
            videoLinks: [
                "test",
                "test",
                "test",
            ],
            pdfLink: [
                "test",
                "test",
                "test",
            ],
        },
    ]
  }),
};
</script>
