/// <reference types="vite/client" />
declare module '*/' {
  function requireAll(context: __WebpackModuleApi.RequireContext): string[];
  export = requireAll;
}