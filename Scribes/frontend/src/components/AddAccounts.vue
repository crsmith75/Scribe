<template>
  <div class ="container margin-top 5">
  <div id="account-form">
        <form @submit.prevent="handleSubmit">
        <label>Twitter Handle</label>
        <input 
            ref="first"
            type="text"
            :class="{ 'has-error': submitting && invalidHandle }"
            v-model="twitteraccount.handle"
            @focus="clearStatus"
            @keypress="clearStatus"
        />
        <label>Twitter ID</label>
        <input 
            type="text"
            :class="{ 'has-error': submitting && invalidTwitterID }"
            v-model="twitteraccount.twitterid"
            @focus="clearStatus" 
        />
        <p v-if="error && submitting" class="error-message">
            Please fill out all required fields
        </p>
        <p v-if="success" class="success-message">
            Account successfully added! Wait Momentarily while the Chain ID is created!
        </p>
        <md-button 
          v-on:click="notify"
          class="md-raised">Add Account</md-button>
        </form>
    </div>
  </div>
</template>


<script>
  export default {
    name: "AddAccounts",
    data() {
      return {
        submitting: false,
        error: false,
        success: false,
        twitteraccount: {
          handle: '',
          twitterid: '',
        },
      }
    },
    computed: {
        invalidHandle() {
            return this.twitteraccount.handle === ''
        },

        invalidTwitterID() {
            return this.twitteraccount.twitterid === ''
        },
    },
    methods: {
        handleSubmit() {
            this.submitting = true
            this.clearStatus()

            if (this.invalidHandle || this.invalidTwitterID) {
            this.error = true
            return
            }

            this.$emit('add:twitteraccount', this.twitteraccount)
            this.$refs.first.focus()
            this.twitteraccount = {
                handle: '',
                twitterid: '',
            }
            this.error = false
            this.success = true
            this.submitting = false
         },
        clearStatus() {
            this.success = false
            this.error = false
        },
        notify: function(event) {
          alert(this.twitteraccount.handle + ' is now being tracked! We will notify you when their tweets begin being Factomized!')
        }
    }
  }
</script>

<style scoped>
  form {
    margin-bottom: 2rem;
  }

  [class*='-message'] {
    font-weight: 500;
  }

  .error-message {
    color: #d33c40;
  }

  .success-message {
    color: #32a95d;
  }
  .md-button {
    background-color: #f56f12;
  }
</style>