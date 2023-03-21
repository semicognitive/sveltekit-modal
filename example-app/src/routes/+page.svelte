<script lang="ts">
  import { enhance } from "$app/forms";
  let message: string | undefined;
  let error: string | undefined;

  function hello_test() {
    return ({ result }: any) => {
      message = result.message;
    };
  }
</script>

<main class="flex">
  <h1 class="text-3xl">Just a test</h1>
  <form
    method="POST"
    action="/api/summarize"
    use:enhance={hello_test}
    on:change={() => ((error = undefined), (message = undefined))}
    class="flex flex-col space-y-2 md:min-w-[28rem] lg:min-w-[32rem] xl:min-w-[36rem] max-w-6xl"
  >
    <button type="submit" class="bg-blue-500 text-white rounded-md p-2"
      >Submit</button
    >
    {#if error}
      <span class="my-auto text-red-500">{error}</span>
    {/if}
    {#if message}
      <div class="h-10" />
      <article class="prose">
        Summary: {@html message}
      </article>
    {/if}
  </form>
</main>
