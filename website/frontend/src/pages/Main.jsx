import { SearchBar } from '../components';
export function Main() {
  return (
    <div>
      <div className="flex flex-col items-center w-screen gap-3 py-4 font-arvo">
        <h1 className="text-xl font-bold ">Find books similar to...</h1>
        <SearchBar />
      </div>
    </div>
  );
}
