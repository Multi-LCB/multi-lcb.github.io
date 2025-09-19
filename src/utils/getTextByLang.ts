import textData from "../data/textData.json";

export const getTextByLang = (key: string, lang: string) => {
  return textData[key]?.[lang] || "";
};
