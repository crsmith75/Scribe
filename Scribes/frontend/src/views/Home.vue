<template>
  <div class="home">
    <div class="container">
    <!-- <div v-for="twitteraccount in twitteraccounts"
          :key="twitteraccount.id">
      <p class = "mb-0"> Account:
        <span>{{ twitteraccount.handle }}</span>
      </p> -->
    <!-- </div> -->

    </div>
  </div>
</template>

<script>
// import { apiService } from "@/common/api.service";
// export default {
//   name: "home",
//   data() {
//     return {
//       twitteraccounts: []
//     }
//   },
//   methods: {
//     async getAccounts() {
//       let endpoint = "/api/twitteraccounts/";
//       apiService(endpoint)
//         .then(data => {
//           this.twitteraccounts.push(...data.results)
//         })
//     }
//   },
//   created() {
//     this.getAccounts()
//     console.log(twitteraccounts)
//   }
// };
</script>