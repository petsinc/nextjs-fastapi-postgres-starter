// "use client";
import {ChatComponent} from "./chatComponent";

type user = {
  userId: number
}
export default async function Chat({userId}: user) {

  return (
    <>
      <ChatComponent userId={userId}/>
    </>
  );
}
