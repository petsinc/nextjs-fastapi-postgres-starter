import Chat from "./chat";
type User = {
  id: number;
  name: string;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {
  console.log("fetch", `${apiUrl}/users/me`);
  const user: User = await fetch(`${apiUrl}/users/me`).then((res) =>
    res.json()
  );
  const userId = user.id

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      Hello, {user.name}!
      <Chat userId={userId}/>
    </main>
  );
}
