
<template>
 
  <div class="navbar-fixed ">
    <nav class="my-navbar">
        <div class="container">
            <div class="nav-wrapper">

                 <router-link
                        :to="{ name: 'home' }"
                        class="left brand-logo"
                    ><span class="white-text">Facticus</span>
                    </router-link>
                <ul class="right hide-on-med-and-down">
                <li>
                    <router-link
                        :to="{ name: 'home' }"
                        class="waves-effect waves-light btn"
                    >Home
                    </router-link>
                </li>
                <li><router-link
                        :to="{ name: 'about' }"
                        class="waves-effect waves-light btn"
                    >About
                    </router-link>
                </li>
                <li>
                    <a class="waves-effect waves-light btn" href="/accounts/logout/">Logout</a>
                </li>
                </ul>
            </div>
        </div>
    </nav>
  </div>
 
</template>


<script>

export default {
    name: "NavbarComponent"
}
</script>


<style>
.my-navbar {
  background-color: #29b6f6  !important;
}
.item {
  background-color: white;
}
.btn {
  background-color: white;
}
.brand-logo {
    font-weight: bold;
    font-size: 130%;
    color: white;
}
.brand-logo:hover {
    color: #f56f12 !important;
}

</style>
