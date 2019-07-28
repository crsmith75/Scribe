<template>
  <div class="home">
    <div class="container">
    <div v-for="twitteraccount in twitteraccounts"
          :key="twitteraccount.pk">
      <p class = "mb-0"> Account:
        <span>{{ twitteraccount.twitter_handle }}</span>
      </p>
    </div>

    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
export default {
  name: "home",
  data() {
    return {
      twitteraccounts: []
    }
  },
  methods: {
    getAccounts() {
      let endpoint = "/api/twitteraccounts/";
      apiService(endpoint)
        .then(data => {
          this.twitteraccounts.push(...data.results)
        })
    }
  },
  created() {
    this.getAccounts()
  }
};
</script>