export function useFormatTipoFuncao() {
  const formatTipoFuncao = (tipo?: string): string => {
    if (!tipo) return "";

    const mapping: Record<string, string> = {
      colaborador: "Colaborador",
      TI: "TI",
      Financiro: "Financeiro",
      Marketing: "Marketing",
      Juridíco: "Jurídico",
      Administrativo: "Administrativo",
      Projeto: "Projeto",
    };

    return mapping[tipo] || tipo;
  };

  return { formatTipoFuncao };
}

